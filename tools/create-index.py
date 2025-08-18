# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "typer",
#     "pyyaml",
# ]
# ///

from __future__ import annotations

import os
import re
from typing import List, NamedTuple

import typer
import yaml

PANDOC_FRONTMATTER = r"""---
author: Niklas Morberg
title: Morbergs receptsamling
date: \today
documentclass: scrbook
classoption:
- titlepage=firstiscover
mainfont: 'Hoefler Text'
sansfont: 'Rockwell'
fontsize: 12pt
lang: sv
papersize: a4
toc-title: Innehåll
header-includes:
- \usepackage{xfrac}
---"""


class Directory(NamedTuple):
    name: str
    files: List[str]


def parse_front_matter(file_path: str) -> tuple[dict, str]:
    """Parse YAML front matter and return metadata + content"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---\n"):
        try:
            front_matter_end = content.find("\n---\n", 4)
            if front_matter_end != -1:
                yaml_content = content[4:front_matter_end]
                metadata = yaml.safe_load(yaml_content) or {}
                markdown_content = content[
                    front_matter_end + 5 :
                ]  # Skip past second ---
                return metadata, markdown_content
        except yaml.YAMLError:
            pass

    return {}, content


def should_include_in_pdf(file_path: str) -> bool:
    """Check if recipe should be included in PDF"""
    metadata, _ = parse_front_matter(file_path)
    return not metadata.get("pdf_exclude", False)


def get_title(file_name: str) -> str:
    """Extracts the recipe title from file_name.

    First tries YAML front matter 'title' field, then falls back to
    first markdown heading.
    """
    metadata, content = parse_front_matter(file_name)

    # Try YAML title first
    if "title" in metadata:
        return metadata["title"]

    # Fall back to first heading
    lines = content.strip().split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()


def get_dirs(root="source/") -> List[Directory]:
    """Returns a sorted list of tuples with directories and
    their file names from source/ directory.

    Directories containing '.git' and current dir will be excluded.
    'Referens' will be last in list.
    """
    dirs = []
    referens = None
    for dir_name, _, files in os.walk(root):
        if ".git" in dir_name or dir_name == root:
            continue
        if dir_name == os.path.join(root, "Referens"):
            referens = Directory(dir_name, files)
        else:
            dirs.append(Directory(dir_name, files))
    dirs.sort()
    return dirs + ([referens] if referens else [])


def print_categories(dirs: List[Directory]):
    """Prints categories, recipe titles and links in markdown format."""
    for dir in dirs:
        category = dir.name.removeprefix("source/")
        print(f"## {category}\n")
        for file in sorted(dir.files):
            file_path = os.path.join(dir.name, file)
            title = get_title(file_path)
            url = file_path.removeprefix("source/")
            print(f"* [{title}]({url})")
        print()


def print_pandoc_categories(dirs: List[Directory]):
    """Generate pandoc markdown file with internal links."""

    def convert_to_anchor_link(filename_to_id, line):
        """Replace relative markdown links to other recipes with anchor
        links."""
        # Matches e.g. ](../any_folder_name/some-file) and changes them into: ](#some-id)
        return re.sub(
            r"\]\(\.\./[^/]+/([^)]+)\)",
            lambda m: f"](#{filename_to_id[m.group(1)]})",
            line,
        )

    def get_heading_id(title: str) -> str:
        """Generate Pandoc heading ID from title."""
        # Lowercase, replace spaces with '-', remove non-alphanum except '-'
        id = re.sub(r"[^\w\- ]", "", title.lower())
        id = id.replace(" ", "-")
        return id

    # Build a mapping from file name (without .md extension) to heading ID
    # Only include files that should be in PDF
    filename_to_id = {}
    for dir in dirs:
        for file in dir.files:
            file_path = os.path.join(dir.name, file)
            if should_include_in_pdf(file_path):
                filename_to_id[file.replace(".md", "")] = get_heading_id(
                    get_title(file_path)
                )

    for dir in dirs:
        category = dir.name.removeprefix("source/")

        # Check if any files in this category should be included
        category_files = [
            file
            for file in dir.files
            if should_include_in_pdf(os.path.join(dir.name, file))
        ]

        if not category_files:
            continue  # Skip empty categories

        print(f"# {category}")
        for file in sorted(category_files):
            file_path = os.path.join(dir.name, file)
            metadata, content = parse_front_matter(file_path)

            # Process the markdown content (skip YAML front matter)
            for line in content.split("\n"):
                line = convert_to_anchor_link(filename_to_id, line + "\n")
                # Indent all headings one step
                if line.startswith("#"):
                    print("#", end="")
                print(line, end="")
            print("\n\\clearpage\n")


def append_skip_colons(in_file: str, out_file: str):
    """Append in_file to out_file. Skip lines starting with ':::' and YAML front matter"""
    metadata, content = parse_front_matter(in_file)

    with open(out_file, "a") as output:
        for line in content.split("\n"):
            if not line.startswith(":::"):
                output.write(line + "\n")


def create_index_file(dir_name: str, sort_order: int, file_name: str = "index.md"):
    """Create index.md in dir_name with YAML header

    Example:
    ---
    layout: default
    title: Bakat
    has_children: true
    nav_order: 2
    ---

    # Bakat
    """
    title = dir_name.removeprefix("docs/")
    header = f"""---
layout: default
title: {title}
has_children: true
nav_order: {sort_order + 2}
---

# {title}
"""
    filename = os.path.join(dir_name, file_name)
    with open(filename, "w") as f:
        f.write(header)


def create_folders(dirs: List[Directory]):
    """Creates subdirectories in 'docs' mirroring 'source'

    Also creates an index.md in each subdirectory.
    """
    dir_names = [dir.name.replace("source/", "docs/") for dir in dirs]
    for sort_order, dir_name in enumerate(dir_names):
        try:
            os.makedirs(dir_name)
        except FileExistsError:
            pass
        create_index_file(dir_name, sort_order)


def jekyll_file_header(input_file: str) -> str:
    """Returns a YAML header based on input_file.

    Uses format from the Jekyll theme Just the Docs.

    Example:

    ---
    layout: default
    title: Bröd i gryta
    parent: Bakat
    ---
    """
    title = get_title(input_file)
    # 'source/Fågel/kyckling.md -> Fågel
    parent = input_file.split("/")[1]
    output = f"""---
layout: default
title: {title}
parent: {parent}
---
"""
    return output


def create_file(filename: str, content: str):
    """Creates filename with content."""
    with open(filename, "w") as f:
        f.write(content)


def create_jekyll_files(input_dirs: List[Directory]):
    """Create Jekyll files in 'docs' directory"""
    for input_dir in input_dirs:
        for file in input_dir.files:
            output_dir = input_dir.name.replace("source/", "docs/")
            output_file = os.path.join(output_dir, file)
            input_file = os.path.join(input_dir.name, file)
            header = jekyll_file_header(input_file)
            create_file(output_file, header)
            append_skip_colons(input_file, output_file)


app = typer.Typer()


@app.command()
def print_index():
    """Generate table of contents markdown file.

    Suitable for a start page with links to all recipes."""

    header = """---
layout: default
title: Morbergs receptsamling
nav_order: 1
---
"""
    print(header)
    print("# Morbergs receptsamling\n")
    dirs = get_dirs()
    print_categories(dirs)


@app.command()
def single_markdown():
    """Generate one markdown file from all files in `source/` dir.

    Use as starting point for pandoc to generate a PDF.
    """
    dirs = get_dirs()
    print(PANDOC_FRONTMATTER)
    print_pandoc_categories(dirs)


@app.command()
def create_docs():
    """Creates docs/ with markdown files suitable for Jekyll."""
    dirs = get_dirs()
    create_folders(dirs)
    create_jekyll_files(dirs)


# %%
if __name__ == "__main__":
    app()

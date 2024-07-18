#!/usr/bin/env python3
# %%
from __future__ import annotations

import os
from typing import List, NamedTuple

import typer

PANDOC_FRONTMATTER = r"""---
author: Niklas Morberg
title: Morbergs receptsamling
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


def get_title(file_name: str) -> str:
    """Extracts the recipe title from file_name.

    Assumes the title of the recipe is first line in file.
    The first line can be formatted as a markdown header.
    """
    with open(file_name, "r") as f:
        title = f.readline().strip("# \n")
        return title


def get_dirs() -> List[Directory]:
    """Returns a sorted list of tuples with directories and
    their file names from source/ directory.

    Directories containing '.git' and current dir will be excluded.

    The directories will be sorted alphabetically with the exception
    of "Referens" which will be last.
    """
    dirs = [
        Directory(dir_name, files)
        for dir_name, _, files in os.walk("source/")
        if ".git" not in dir_name  # exclude *.git* directories
        if dir_name != "source/"  # exclude root dir
        if dir_name != "source/Referens"
    ]
    dirs.sort()
    referens = [
        Directory(dir_name, files)
        for dir_name, _, files in os.walk("source/")
        if dir_name == "source/Referens"
    ]
    return dirs + referens


def print_categories(dirs: List[Directory]):
    """Prints categories, recipe titles and links in markdown format."""
    for dir in dirs:
        category = dir.name.removeprefix("source/")
        print(f"## {category}\n")
        for file in sorted(dir.files):
            file_path = dir.name + "/" + file
            title = get_title(file_path)
            url = file_path.removeprefix("source/")
            print(f"* [{title}]({url})")
        print()


def print_pandoc_categories(dirs: List[Directory]):
    """Generate pandoc markdown file.

    Used as starting point for pandoc to generate a PDF.
    """
    for dir in dirs:
        category = dir.name.removeprefix("source/")
        print(f"# {category}")
        for file in sorted(dir.files):
            file_path = dir.name + "/" + file
            lines = open(file_path).readlines()
            for line in lines:
                # Indent all headers one step
                if line[0] == "#":
                    print("#", end="")
                print(line, end="")
            print("\n\\clearpage\n")


def append_skip_colons(in_file: str, out_file: str):
    """Append in_file to out_file. Skip lines starting with ':::'"""
    with open(in_file, "r") as input, open(out_file, "a") as output:
        for line in input:
            if not line.startswith(":::"):
                output.write(line)


def create_index_file(dir_name: str, sort_order: int):
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
    filename = dir_name + "/index.md"
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
            output_file = output_dir + "/" + file
            input_file = input_dir.name + "/" + file
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
def print_pandoc_index():
    """Generate pandoc markdown file from source/ dir.

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

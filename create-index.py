#!/usr/bin/env python3
# %%
from __future__ import annotations

import os
from typing import List, NamedTuple

import typer

PANDOC_FRONTMATTER = """---
author: Niklas Morberg
title: Morbergs receptsamling
documentclass: scrreprt
mainfont: 'Hoefler Text'
sansfont: 'Avenir'
papersize: a4paper
toc-title: Innehåll
---"""
PANDOC_REFERENCE_FRONTMATTER = """---
author: Niklas Morberg
title: Referens
documentclass: scrreprt
mainfont: 'Hoefler Text'
sansfont: 'Avenir'
papersize: a4paper
toc-title: Referens
---"""
PANDOC_PRE_FILE_PATH = "``` {.include shift-heading-level-by=1}"
PANDOC_POST_FILE_PATH = """```
\clearpage"""


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
    their file names from current directory.

    Directories containing '.git' and current dir will be excluded.

    The directories will be sorted alphabetically with the exception
    of "Referens" which will be last.
    """
    dirs = [
        Directory(dir_name, files)
        for dir_name, _, files in os.walk(".")
        if ".git" not in dir_name  # exclude *.git* directories
        if dir_name != "."  # exclude root dir
        if dir_name != "./Referens"
    ]
    dirs.sort()
    referens = [
        Directory(dir_name, files)
        for dir_name, _, files in os.walk(".")
        if dir_name == "./Referens"
    ]
    return dirs + referens


def print_categories(dirs: List[Directory]):
    """Prints categories, recipe titles and links in markdown format."""
    for dir in dirs:
        category = dir.name.strip("./")
        print(f"## {category}\n")
        for file in sorted(dir.files):
            file_path = dir.name + "/" + file
            title = get_title(file_path)
            print(f"* [{title}]({file_path})")
        print()


def print_pandoc_categories(dirs: List[Directory]):
    """Generate pandoc markdown file

    Use as starting point for pandoc to generate a PDF.

    Directory 'Referens' will be excluded. This dir contains pages
    with tables not possible to render in twocolumn layout.
    """
    for dir in dirs:
        category = dir.name.strip("./")
        print(f"# {category}")
        for file in sorted(dir.files):
            file_path = dir.name + "/" + file
            print(PANDOC_PRE_FILE_PATH)
            print(file_path)
            print(PANDOC_POST_FILE_PATH)


app = typer.Typer()


@app.command()
def print_index():
    """Generate table of contents markdown file.

    Suitable for a start page with links to all recipes."""
    print("# Morbergs receptsamling\n")
    dirs = get_dirs()
    print_categories(dirs)


@app.command()
def print_pandoc_index():
    """Generate pandoc markdown file

    Use as starting point for pandoc to generate a PDF.

    Directory 'Referens' will be excluded. This dir contains pages
    with tables not possible to render in twocolumn layout.
    """
    dirs = get_dirs()
    two_column_dirs = [dir for dir in dirs if dir.name != "./Referens"]
    print(PANDOC_FRONTMATTER)
    print_pandoc_categories(two_column_dirs)


@app.command()
def print_pandoc_reference():
    """Generate pandoc markdown file for Referens directory only.

    Use as starting point for pandoc to generate a PDF.

    'Referens' contains pages with tables not possible to render in
    twocolumn layout.
    """
    dirs = get_dirs()
    reference_dir = [dir for dir in dirs if dir.name == "./Referens"]
    print(PANDOC_REFERENCE_FRONTMATTER)
    print_pandoc_categories(reference_dir)


# %%
if __name__ == "__main__":
    app()

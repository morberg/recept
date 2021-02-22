#!/usr/bin/env python3
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
classoption: twocolumn
toc-title: Innehåll
---
"""


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
    """
    dirs = [
        Directory(dir_name, files)
        for dir_name, _, files in os.walk(".")
        if ".git" not in dir_name  # exclude *.git* directories
        if dir_name != "."  # exclude root dir
    ]
    dirs.sort()
    return dirs


def print_categories():
    """Prints categories, recipe titles and links in markdown format."""
    dirs = get_dirs()
    for dir in dirs:
        category = dir.name.strip("./")
        print(f"## {category}\n")
        for file in sorted(dir.files):
            file_path = dir.name + "/" + file
            title = get_title(file_path)
            print(f"* [{title}]({file_path})")
        print()


app = typer.Typer()


@app.command()
def print_index():
    print("# Morbergs receptsamling\n")
    print_categories()
    print("## [Sous Vide](sous-vide.md)")


@app.command()
def write_pandoc_index(output: str = "receptsamling.md"):
    with open(output, "w") as f:
        f.write(PANDOC_FRONTMATTER)
        dirs = get_dirs()
        for dir in dirs:
            category = dir.name.strip("./")
            f.write(f"\n# {category}\n")
            for file in sorted(dir.files):
                file_path = dir.name + "/" + file
                f.write(
                    f"""``` {{.include shift-heading-level-by=1}}
{file_path}
```
\clearpage
"""
                )


if __name__ == "__main__":
    app()

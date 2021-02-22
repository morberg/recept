#!/usr/bin/env python3
from __future__ import annotations

import os
from typing import List, NamedTuple


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
    file_list = [
        Directory(dir_name, files)
        for dir_name, _, files in os.walk(".")
        if ".git" not in dir_name  # exclude *.git* directories
        if dir_name != "."  # exclude root dir
    ]
    file_list.sort()
    return file_list


def print_categories():
    """Prints categories, recipe titles and links in markdown format."""
    dirs = get_dirs()
    for dir in dirs:
        category = dir.name.strip("./")
        print(f"## {category}\n")
        for file in sorted(dir.files):
            file_name = dir.name + "/" + file
            title = get_title(file_name)
            print(f"* [{title}]({file_name})")
        print()


print("# Morbergs receptsamling\n")
print_categories()
print("## [Sous Vide](sous-vide.md)")

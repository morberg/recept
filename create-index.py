#!/usr/bin/env python3
import os


def get_title(file_name):
    """Extracts the recipe title from file_name.

    Assumes the title of the recipe is first line in file.
    The first line can be formatted as a markdown header.
    """
    with open(file_name, "r") as f:
        title = f.readline().strip("# \n")
        return title


def get_file_list():
    """Returns a sorted list of tuples with directories and
    their file names from current directory.

    Directories containing '.git' and current dir will be excluded.
    """
    file_list = [
        (dir, files)
        for dir, _, files in os.walk(".")
        if ".git" not in dir  # exclude *.git* directories
        if dir != "."  # exclude root dir
    ]
    file_list.sort()
    return file_list


def print_categories():
    """Prints categories, recipe titles and links in markdown format."""
    file_list = get_file_list()
    for dir, files in file_list:
        category = dir.strip("./")
        print(f"## {category}\n")
        for file in sorted(files):
            file_name = dir + "/" + file
            title = get_title(file_name)
            print(f"* [{title}]({file_name})")
        print()


print("# Morbergs receptsamling\n")
print_categories()
print("## [Sous Vide](sous-vide.md)")

#!/usr/bin/env python3
# Create a receptsamling.md file to be used by pandoc
import os

rootDir = "."
with open("receptsamling.md", "w") as f:
    f.write(
        """---
author: Niklas Morberg
title: Morbergs receptsamling
---
"""
    )

    for dirName, subdirList, fileList in os.walk(rootDir):
        subdirList.sort()
        if ".git" in subdirList:
            subdirList.remove(".git")
        if ".github" in subdirList:
            subdirList.remove(".github")
        if dirName == ".":
            continue
        category = dirName
        f.write("\n# {}\n".format(category[2:]))
        for fname in sorted(fileList):
            recipeLink = fname
            with open(dirName + "/" + fname, "r") as read_file:
                recipeTitle = read_file.readline().strip("#").strip()
            f.write("``` {.include shift-heading-level-by=1}\n")
            f.write("{}/{}\n".format(dirName, recipeLink))
            f.write("```\n")
            f.write("\\clearpage\n")

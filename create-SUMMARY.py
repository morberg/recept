#!/usr/bin/env python3
# Create a SUMMARY.md file to be used by mdbook
import os

rootDir = "."
with open("SUMMARY.md", "w") as f:
    f.write("# Morbergs receptsamling\n")

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
            f.write("* [{}]({}/{})\n".format(recipeTitle, category, recipeLink))

    f.write("# Sous Vide\n")
    f.write("- [Sous Vide](./sous-vide.md)")

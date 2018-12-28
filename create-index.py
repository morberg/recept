#!/usr/bin/env python3
import os

rootDir = '.'

print("# Morbergs receptsamling")

for dirName, subdirList, fileList in os.walk(rootDir):
    subdirList.sort()
    if '.git' in subdirList:
        subdirList.remove('.git')
    if (dirName == '.'):
        continue
    category = dirName
    print("\n## {}\n".format(category[2:]))
    for fname in sorted(fileList):
        recipeLink = fname
        with open(dirName + '/' + fname, 'r') as f:
                recipeTitle = f.readline().strip('#').strip()
        print("* [{}]({}/{})".format(recipeTitle, category, recipeLink))

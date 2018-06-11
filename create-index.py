#!/usr/bin/env python3
import os
import unicodedata

rootDir = '.'

print("# Morbergs receptsamling")

for dirName, subdirList, fileList in os.walk(rootDir):
    subdirList.sort()
    if '.git' in subdirList:
        subdirList.remove('.git')
    if (dirName == '.'):
        continue
    # normalize not needed for APFS introduced in macOS 10.13
    category = unicodedata.normalize('NFC', dirName)
    print("\n## {}\n".format(category[2:]))
    for fname in sorted(fileList):
        recipeLink = unicodedata.normalize('NFC', fname)
        with open(dirName + '/' + fname, 'r') as f:
                recipeTitle = f.readline().strip('#').strip()
        print("* [{}]({}/{})".format(recipeTitle, category, recipeLink))

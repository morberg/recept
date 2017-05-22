#!/usr/bin/env python3
import os
import unicodedata

rootDir = '.'

print("# Morbergs receptsamling")

for dirName, subdirList, fileList in os.walk(rootDir):
    if '.git' in subdirList: subdirList.remove('.git')
    if (dirName=='.'): continue
    category = unicodedata.normalize('NFC', dirName)
    print("\n## {}\n".format(category[2:]))
    for fname in fileList:
        recipe = unicodedata.normalize('NFC', fname)
        print("* [{}]({}/{})".format(recipe[:-3], dirName, recipe))
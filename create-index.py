#!/usr/bin/env python3
import os

rootDir = '.'

print("# Morbergs receptsamling")

for dirName, subdirList, fileList in os.walk(rootDir):
    if '.git' in subdirList: subdirList.remove('.git')
    print("## {}".format(dirName[2:]))
    for fname in fileList:
        print("[{}]({}/{})".format(fname[:-3], dirName, fname))
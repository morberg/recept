#!/bin/bash
echo "# Morbergs receptsamling"
for D in `find . -type d -not -path "*.git*" -not -name "."`
do
	echo "## ${D:2}"
	for F in `find $D -type f`
	do
		recipe=${F##*/}
		echo "* [${recipe%.md*}]($F)"
	done
done

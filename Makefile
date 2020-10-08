pdf: receptsamling.pdf sous-vide.pdf

receptsamling.pdf: receptsamling.md create-receptsamling.py
	pandoc receptsamling.md \
	--lua-filter=include-files.lua \
	--pdf-engine=xelatex --variable documentclass=scrreprt \
	--toc --toc-depth=2 --variable toc-title="Innehåll" \
	--variable mainfont="Hoefler Text" --variable sansfont="Avenir" \
	--variable papersize=a4paper \
	--variable classoption=twocolumn \
	-o receptsamling.pdf

sous-vide.pdf: sous-vide.md
	pandoc sous-vide.md \
	--pdf-engine=xelatex --variable documentclass=scrreprt \
	--variable mainfont="Hoefler Text" --variable sansfont="Avenir" \
	--variable papersize=a4paper \
	-o sous-vide.pdf

receptsamling.md: */*.md
	python create-receptsamling.py

.PHONY: clean
clean:
	rm -f sous-vide.pdf
	rm -f receptsamling.pdf

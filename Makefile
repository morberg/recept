pdf: receptsamling.pdf sous-vide.pdf

receptsamling.pdf:
	pandoc */*.md \
	--pdf-engine=xelatex --variable documentclass=scrreprt \
	--toc --toc-depth=1 --variable toc-title="Innehåll" \
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

.PHONY: clean
clean:
	rm -f sous-vide.pdf
	rm -f receptsamling.pdf
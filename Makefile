pdf:
	pandoc */*.md sous-vide.md \
	--pdf-engine=xelatex --variable documentclass=scrreprt \
	--toc --toc-depth=1 --variable toc-title="Innehåll" \
	--variable mainfont="Hoefler Text" --variable sansfont="Avenir" \
	--variable papersize=a4paper \
	-o receptsamling.pdf

twocolumn:
	pandoc */*.md \
	--pdf-engine=xelatex --variable documentclass=scrreprt \
	--toc --toc-depth=1 --variable toc-title="Innehåll" \
	--variable mainfont="Hoefler Text" --variable sansfont="Avenir" \
	--variable papersize=a4paper \
	--variable classoption=twocolumn \
	-o receptsamling.pdf

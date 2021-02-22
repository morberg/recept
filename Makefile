pdf: receptsamling.pdf sous-vide.pdf

receptsamling.pdf: receptsamling.md
	pandoc receptsamling.md \
	--lua-filter=include-files.lua \
	--pdf-engine=xelatex \
	--toc --toc-depth=2 \
	-o receptsamling.pdf

sous-vide.pdf: sous-vide.md
	pandoc sous-vide.md \
	--pdf-engine=xelatex \
	-o sous-vide.pdf

receptsamling.md: */*.md create-index.py
	python create-index.py write-pandoc-index

.PHONY: clean
clean:
	rm -f sous-vide.pdf
	rm -f receptsamling.pdf

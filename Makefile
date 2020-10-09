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

receptsamling.md: */*.md create-receptsamling.py
	python create-receptsamling.py

.PHONY: clean
clean:
	rm -f sous-vide.pdf
	rm -f receptsamling.pdf

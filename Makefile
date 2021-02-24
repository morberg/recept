pdf: receptsamling.pdf referens.pdf

receptsamling.pdf: receptsamling.md
	pandoc receptsamling.md \
	--lua-filter=include-files.lua \
	--lua-filter=columns.lua \
	--pdf-engine=xelatex \
	--toc --toc-depth=2 \
	-o receptsamling.pdf

referens.pdf: referens.md
	pandoc referens.md \
	--lua-filter=include-files.lua \
	--pdf-engine=xelatex \
	-o referens.pdf

index.md: */*.md create-index.py
	python create-index.py print-index > index.md

receptsamling.md: */*.md create-index.py
	python create-index.py print-pandoc-index > receptsamling.md

referens.md: Referens/*.md create-index.py
	python create-index.py print-pandoc-reference > referens.md


.PHONY: clean
clean:
	rm -f referens.pdf
	rm -f receptsamling.pdf

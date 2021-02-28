pdf: receptsamling.pdf

jekyll: source/*/*.md index.md
	python tools/create-index.py create-docs
	cp source/_config.yml docs/

receptsamling.pdf: receptsamling.md tools/format.tex
	pandoc receptsamling.md \
	--lua-filter=tools/include-files.lua \
	--lua-filter=tools/columns.lua \
	--include-before-body=tools/format.tex \
	--pdf-engine=xelatex \
	--toc --toc-depth=2 \
	-o pdf/receptsamling.pdf

receptsamling.tex: receptsamling.md
	pandoc receptsamling.md \
	--lua-filter=tools/include-files.lua \
	--lua-filter=tools/columns.lua \
	--include-before-body=tools/format.tex \
	--pdf-engine=xelatex \
	--standalone \
	--toc --toc-depth=2 \
	-o pdf/receptsamling.tex


index.md: source/*/*.md tools/create-index.py
	mkdir -p docs
	python tools/create-index.py print-index > docs/index.md

receptsamling.md: source/*/*.md tools/create-index.py
	python tools/create-index.py print-pandoc-index > receptsamling.md


.PHONY: clean
clean:
	rm -f pdf/receptsamling.pdf
	rm -f receptsamling.md
	rm -rf docs
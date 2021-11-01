PANDOC_FLAGS = --lua-filter=tools/include-files.lua \
	--lua-filter=tools/xfrac.lua \
	--lua-filter=tools/columns.lua \
	--template=tools/recipe-template.tex \
	--include-before-body=tools/format.tex \
	--pdf-engine=xelatex \
	--toc --toc-depth=2

all: jekyll pdf

pdf: receptsamling.pdf

tex: receptsamling.tex

jekyll: source/*/*.md source/* index.md
	python tools/create-index.py create-docs
	cp source/_config.yml docs/
	cp source/*.png docs/
	cp source/favicon.ico docs/

receptsamling.pdf: pdf/receptsamling.md tools/format.tex
	pandoc pdf/receptsamling.md \
	$(PANDOC_FLAGS) \
	-o pdf/receptsamling.pdf

receptsamling.tex: pdf/receptsamling.md tools/format.tex
	pandoc pdf/receptsamling.md \
	$(PANDOC_FLAGS) \
	-o pdf/receptsamling.tex


index.md: source/*/*.md tools/create-index.py
	mkdir -p docs
	python tools/create-index.py print-index > docs/index.md

pdf/receptsamling.md: source/*/*.md tools/create-index.py
	python tools/create-index.py print-pandoc-index > pdf/receptsamling.md


.PHONY: clean
clean:
	rm -f pdf/*
	rm -f receptsamling.md
	rm -rf docs
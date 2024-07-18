LUA_FLAGS = --lua-filter=tools/xfrac.lua \
	--lua-filter=tools/columns.lua \
	--toc --toc-depth=2

LATEX_FLAGS = --template=tools/recipe-template.tex \
	--include-before-body=tools/format.tex \
	--pdf-engine=xelatex

all: jekyll pdf

jekyll: source/*/*.md source/* index.md
	python tools/create-index.py create-docs
	cp source/_config.yml docs/
	cp source/*.png docs/
	cp source/favicon.ico docs/

pdf: pdf/receptsamling.pdf

pdf/receptsamling.pdf: pdf/receptsamling.md tools/*
	pandoc pdf/receptsamling.md \
	$(LUA_FLAGS) \
	$(LATEX_FLAGS) \
	-o pdf/receptsamling.pdf

tex: pdf/receptsamling.tex 

pdf/receptsamling.tex: pdf/receptsamling.md tools/format.tex
	pandoc pdf/receptsamling.md \
	$(LUA_FLAGS) \
	$(LATEX_FLAGS) \
	-o pdf/receptsamling.tex

index.md: source/*/*.md tools/create-index.py
	mkdir -p docs
	python tools/create-index.py print-index > docs/index.md

pdf/receptsamling.md: source/*/*.md tools/create-index.py
	python tools/create-index.py print-pandoc-index > pdf/receptsamling.md


.PHONY: clean
clean:
	rm -f pdf/*
	rm -rf docs
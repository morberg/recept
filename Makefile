pdf: receptsamling.pdf

jekyll: source/*/*.md index.md
	cp -r source/ docs/

receptsamling.pdf: receptsamling.md
	pandoc receptsamling.md \
	--lua-filter=tools/include-files.lua \
	--lua-filter=tools/columns.lua \
	--pdf-engine=xelatex \
	--toc --toc-depth=2 \
	-o pdf/receptsamling.pdf

index.md: source/*/*.md tools/create-index.py
	python tools/create-index.py print-index > docs/index.md

receptsamling.md: source/*/*.md tools/create-index.py
	python tools/create-index.py print-pandoc-index > receptsamling.md


.PHONY: clean
clean:
	rm -f pdf/receptsamling.pdf
	rm -f receptsamling.md
	rm -f receptsamling.html
	rm -f index.md

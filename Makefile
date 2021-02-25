pdf: receptsamling.pdf

jekyll: source/*/*.md jekyll/index.md
	cp -r source/ jekyll/

receptsamling.pdf: receptsamling.md
	pandoc receptsamling.md \
	--lua-filter=tools/include-files.lua \
	--lua-filter=tools/columns.lua \
	--pdf-engine=xelatex \
	--toc --toc-depth=2 \
	-o pdf/receptsamling.pdf

jekyll/index.md: source/*/*.md tools/create-index.py
	python tools/create-index.py print-index > jekyll/index.md

receptsamling.md: source/*/*.md tools/create-index.py
	python tools/create-index.py print-pandoc-index > receptsamling.md


.PHONY: clean
clean:
	rm -f pdf/receptsamling.pdf
	rm -f receptsamling.md
	rm -f receptsamling.html
	rm -f index.md

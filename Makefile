package = ../cloud_scanner_generic

sphinx:
	cd docs && \
	make clean && \
	sphinx-apidoc -f -o source/generated $(package) && \
	make html

ghpages:
	-git checkout gh-pages && \
	mv docs/build/html new-docs && \
	rm -rf docs && \
	mv new-docs docs && \
	cp -r docs/* . && \
	rm -rf docs && \
	touch .nojekyll && \
	git add . && \
	git commit -m "Updated generated Sphinx documentation"

MODULE=zetalibrary
SPHINXBUILD=sphinx-build
ALLSPHINXOPTS= -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
BUILDDIR=_build


.PHONY: clean
clean:
	sudo rm -rf build dist $(MODULE).egg-info/ docs/_build
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete

.PHONY: register
register:
	python setup.py register

.PHONY: upload
upload: doc
	python setup.py sdist upload || echo 'Upload already'

.PHONY: test
test: audit
	python setup.py test

.PHONY: audit
audit:
	pylama $(MODULE) -i E501

.PHONY: doc
doc:
	python setup.py build_sphinx --source-dir=docs/ --build-dir=docs/_build --all-files
	python setup.py upload_sphinx --upload-dir=docs/_build/html

.PHONY: pep8
pep8:
	find $(MODULE) -name "*.py" | xargs -n 1 autopep8 -i

MODULE=zetalibrary

clean:
	sudo rm -rf build dist $(MODULE).egg-info/
	find . -name "*.pyc" -delete

install: remove _install clean

register: _register clean

remove:
	sudo pip uninstall $(MODULE) -y

upload: _upload install _commit doc

test:
	python $(MODULE)/tests/__init__.py

_upload:
	python setup.py sdist upload

_commit:
	git add .
	git add . -u
	git commit || echo 'No commits'
	git push origin
	git push intaxi

_register:
	python setup.py register

_install:
	sudo pip install -U .

doc:
	python setup.py build_sphinx --source-dir=docs/ --build-dir=docs/_build --all-files
	python setup.py upload_sphinx --upload-dir=docs/_build/html

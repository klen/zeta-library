MODULE=zetalibrary

clean:
	sudo rm -rf build dist $(MODULE).egg-info/
	find . -name "*.pyc" -delete

install: remove _install clean

register: _register clean

upload: _upload install _commit

_upload:
	python setup.py sdist upload

_commit:
	git add .
	git add . -u
	git commit
	git push origin
	git push intaxi

_register:
	python setup.py register

remove:
	sudo pip uninstall $(MODULE)

_install:
	sudo pip install -U .

test:
	python $(MODULE)/tests/__init__.py

.PHONY: help lint test package sdist wheel install install-user remove clean

help:
	@echo "usage: make <target> [<target> ...]"
	@echo "targets:"
	@echo "  help         - display targets"
	@echo "  lint         - run python linter"
	@echo "  test         - run unit tests"
	@echo "  package      - build distribution files"
	@echo "  sdist        - create source distribution file"
	@echo "  wheel        - create wheel distribution file"
	@echo "  install      - install package, global (requires root)"
	@echo "  install-user - install package, user"
	@echo "  remove       - uninstall package"
	@echo "  clean        - remove generated files"

lint:
	pyflakes avdb/*.py

test:
	#python -m test.test_<name> -v

package: sdist wheel

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

install:
	pip install --upgrade --no-deps --no-index .

install-user:
	pip install --user --upgrade --no-deps --no-index .

remove:
	pip uninstall -y avdb

clean:
	-rm -f *.pyc test/*.pyc avdb/*.pyc
	-rm -fr avdb.egg-info/ build/ dist/ MANIFEST

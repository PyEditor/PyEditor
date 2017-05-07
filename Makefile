BROWSER ?= xdg-open
PYTHON_PACKAGE = pyeditor
TESTS_PACKAGE = tests

.PHONY: clean clean-test clean-pyc clean-build docs help requirements

## remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test

## remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

## remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

## remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr reports/

## run tests quickly with the default Python
test:
	py.test -v tests/

## run tests on every Python version with tox
test-all:
	tox

## run style checks and static analysis with pylint
pylint:
	@-mkdir -p reports/
	@-pylint -f html $(PYTHON_PACKAGE) $(TESTS_PACKAGE) > reports/pylint.html
	@$(BROWSER) reports/pylint.html
	pylint $(PYTHON_PACKAGE) $(TESTS_PACKAGE)

## run style checks and static analysis with flake8
flake8:
	flake8 $(PYTHON_PACKAGE) $(TESTS_PACKAGE)

## check docstring presence and style conventions with pydocstyle
docstrings:
	pydocstyle $(PYTHON_PACKAGE)

lint: flake8 docstrings pylint

## check code coverage quickly with the default Python
coverage:
	@-mkdir -p reports/htmlcov
	coverage run --source $(PYTHON_PACKAGE) `which py.test`
	coverage report -m
	@coverage html -d reports/htmlcov
	@$(BROWSER) reports/htmlcov/index.html

## print code metrics with radon
metrics:
	radon raw -s $(PYTHON_PACKAGE) $(TEST_PACKAGE)
	radon cc -s $(PYTHON_PACKAGE) $(TEST_PACKAGE)
	radon mi -s $(PYTHON_PACKAGE) $(TEST_PACKAGE)

## generate Sphinx HTML documentation, including API docs
docs:
	rm -f docs/$(PYTHON_PACKAGE).rst
	sphinx-apidoc --no-toc -o docs/ $(PYTHON_PACKAGE)
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

## pip-compile requirements templates
requirements:
	$(MAKE) -C requirements all

## package and upload a release to PyPi
publish: clean
	python setup.py publish

## builds source and wheel package
dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

## install the package to the active Python's site-packages
install: clean
	python setup.py install

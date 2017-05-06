REQUIREMENTS_SOURCES := $(wildcard *.in)
REQUIREMENTS := $(REQUIREMENTS_SOURCES:.in=.txt)
PIP_INDEX_URL ?= https://pypi.python.org/simple

dev.txt: base.txt

prod.txt: base.txt

%.txt: %.in
	pip-compile \
	    --verbose \
	    --rebuild \
	    --index-url $(PIP_INDEX_URL) \
	    --output-file $@ $<

all: $(REQUIREMENTS)

check:
	@which pip-compile > /dev/null

clean: check
	rm -f *.txt

.PHONY: all check clean

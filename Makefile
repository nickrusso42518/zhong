# Author: Nick Russo
# Purpose: Provide simple "make" targets for developers
# See README for details about each target.

# Default goal runs the "all" target
.DEFAULT_GOAL := all

.PHONY: all
all: clean lint run

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs black --line-length 80 --check
	@echo "Completed lint"

.PHONY: run
run:
	@echo "Starting  run"
	echo $$'.\n' | python play.py && echo
	echo $$'.\n' | python play.py -i inputs/tp.csv && echo
	echo $$'.\n' | python play.py -m && echo
	echo $$'\n.\n' | python play.py -m -r 100 && echo
	echo $$',\n.\n' | python play.py -q && echo
	python play.py -q -m || test $$? -eq 2
	@echo "Completed run"

.PHONY: clean
clean:
	@echo "Starting  clean"
	find . -name "*.pyc" | xargs rm
	@echo "Starting  clean"

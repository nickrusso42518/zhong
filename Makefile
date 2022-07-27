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
	python play.py < test_stdin/enter_period.txt
	python play.py -i inputs/tp.csv < test_stdin/comma_period.txt
	python play.py -q < test_stdin/enter_period.txt
	python play.py -m -r 200 < test_stdin/bad_period.txt
	python play.py -q -m || test $$? -eq 2
	@echo "Completed run"

.PHONY: clean
clean:
	@echo "Starting  clean"
	find . -name "*.pyc" | xargs rm
	@echo "Starting  clean"

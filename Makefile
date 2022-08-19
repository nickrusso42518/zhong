# Author: Nick Russo
# Purpose: Provide simple "make" targets for developers
# See README for details about each target.

# Default goal runs the "all" target
.DEFAULT_GOAL := all

.PHONY: all
all: clean lint db run

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.py" | xargs black --line-length 80 --check
	find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs bandit --configfile bandit_cfg.yml
	@echo "Completed lint"

.PHONY: db
db:
	@echo "Starting  db"
	python test_lookups.py inputs/default.csv inputs/tp.csv >> /dev/null
	python utils/fileio.py inputs/default.csv inputs/tp.csv
	@echo "Completed db"

.PHONY: run
run:
	@echo "Starting  run"
	python play.py < test_stdin/enter_period.txt
	python play.py -i inputs/tp.csv < test_stdin/comma_period.txt
	python play.py -s < test_stdin/period.txt
	python play.py -c < test_stdin/period.txt
	python play.py -p < test_stdin/qmark_period.txt
	python play.py -s -c < test_stdin/period.txt
	python play.py -s -p < test_stdin/qmark_period.txt
	python play.py -c -r 200 < test_stdin/bad_period.txt
	python play.py -s -c -p || test $$? -eq 2
	python play.py -i inputs/nonexist.csv || test $$? -eq 3
	@echo "Completed run"

.PHONY: clean
clean:
	@echo "Starting  clean"
	find . -name "*.pyc" | xargs rm
	@echo "Completed clean"

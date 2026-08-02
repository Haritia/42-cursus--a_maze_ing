
CONFIG = config.txt
VENV = .mazenv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
FLAGS = --warn-return-any\
		--warn-unused-ignores\
		--ignore-missing-imports\
		--disallow-untyped-defs\
		--check-untyped-defs

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	
run: install
	$(PYTHON) a_maze_ing.py $(CONFIG)

lint: install
	$(PYTHON) -m flake8 --exclude=$(VENV) . 
	$(PYTHON) -m mypy --exclude=$(VENV) $(FLAGS) .

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} \;
	find . -type d -name ".mypy_cache" -exec rm -rf {} \;

debug:
	$(PYTHON) -m pdb a_maze_ing.py

lint-strict:
	$(PYTHON) -m flake8 --exclude=$(VENV) . 
	$(PYTHON) -m mypy --strict --exclude=$(VENV) .

build:
	$(PYTHON) -m build
	mv dist/*.whl .
	rm -rf dist
	$(PIP) install *.whl

.PHONY: install run lint link-strict clean debug build
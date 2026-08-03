CONFIG = config.txt
VENV = .mazenv
PYTHON = $(VENV)/bin/python3
MAIN = a_maze_ing.py
PIP = $(VENV)/bin/pip
FLAGS = --warn-return-any\
		--warn-unused-ignores\
		--ignore-missing-imports\
		--disallow-untyped-defs\
		--check-untyped-defs

install:
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . | grep "__pycache__" | xargs -I {} rm -rf {}
	find . -name ".mypy_cache" -type d | xargs rm -rf
	rm -rf $(VENV)

lint:
	$(PYTHON) -m flake8 --docstring google --exclude=$(VENV) .
	$(PYTHON) -m mypy --exclude=$(VENV) $(FLAGS) .

lint-strict:
	$(PYTHON) -m flake8 --docstring google --exclude=$(VENV) .
	$(PYTHON) -m mypy --strict --exclude=$(VENV) .

build: install
	$(PYTHON) -m build
	mv dist/*.whl .
	mv dist/*.tar.gz .
	rm -rf dist
	$(PIP) install *.whl

.PHONY: install run lint link-strict clean debug build

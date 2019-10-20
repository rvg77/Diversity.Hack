DATA_DIRECTORY = ./data/input/
OUTPUT_DIRECTIORY = ./data/output/

DATA_PREFICS = _input.json
SOLUTION_PREFICS = _solution_output.json

PYTHON = python

DF = data/input/contest_input.json

all: test

test:
	$(PYTHON) main.py --data "$(DF)" --output "$(OUTPUT_DIRECTIORY)"


PYTHON=python



install:
	$(PYTHON) ./setup.py install

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"


PYTHON=python3.9



install:
	$(PYTHON) ./setup.py install

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

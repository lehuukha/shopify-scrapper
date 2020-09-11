.PHONY: install run check

# Install virtual env
install:
	pipenv install

# Run script
run:
	pipenv run python src/main.py -i tmp/stores.csv -o tmp/output.csv

# Check code analysis
check:
	pipenv run pylint src/main.py

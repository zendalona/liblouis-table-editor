.PHONY: run cleanmake 
PYTHON=python3

install:
	pip install -r requirements.txt

run:
	@$(PYTHON) src/main.py

clean:
	@echo "Cleaning up..."
	# Add commands to clean up files if necessary

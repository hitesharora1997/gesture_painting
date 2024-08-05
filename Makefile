# Variables
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
PYTEST = $(VENV_NAME)/bin/pytest
FLASK = $(VENV_NAME)/bin/flask

.PHONY: all setup install run clean docker help

# Default target
all: clean setup install run

# Create virtual environment and install dependencies
setup:
	@echo "Setting up the virtual environment and installing dependencies."
	python3 -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt

# Install dependencies
install: $(VENV_NAME)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

# Run the application
run:
	@echo "Running the application..."
	python gesture_painting.py

# Run tests
test: install
	@echo "Running tests..."
	PYTHONPATH=$(PWD) $(PYTEST) tests

# Build Docker image
docker:
	@echo "Building Docker image..."
	docker build -t gesture_painting .


# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

# Display help information
help:
	@echo "Usage: make [TARGET]"
	@echo ""
	@echo "Targets:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  install   - Install dependencies"
	@echo "  run       - Run the application"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean up"
	@echo "  docker    - Build Docker image"
	@echo "  help      - Show this help message"
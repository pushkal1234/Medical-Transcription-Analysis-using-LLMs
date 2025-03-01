.PHONY: setup install test run clean

# Default target
all: setup install

# Setup the project
setup:
	@echo "Setting up the project..."
	python -m pip install --upgrade pip
	python -m pip install -e .

# Install dependencies
install:
	@echo "Installing dependencies..."
	python -m pip install -r requirements.txt

# Run tests
test:
	@echo "Running tests..."
	python tests/test_installation.py

# Run the API server
run:
	@echo "Starting the API server..."
	python src/main.py

# Clean temporary files
clean:
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf src/medical_transcription/__pycache__/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Create a virtual environment
venv:
	@echo "Creating virtual environment..."
	python -m venv venv
	@echo "Activate with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"

# Install development dependencies
dev-install:
	@echo "Installing development dependencies..."
	python -m pip install -r requirements.txt
	python -m pip install pytest black flake8 isort

# Format code
format:
	@echo "Formatting code..."
	black src/ tests/ examples/
	isort src/ tests/ examples/

# Lint code
lint:
	@echo "Linting code..."
	flake8 src/ tests/ examples/

# Run example script
example:
	@echo "Running example script..."
	python examples/process_audio.py $(AUDIO_FILE) --output-dir output

# Help
help:
	@echo "Available targets:"
	@echo "  setup        - Set up the project"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests"
	@echo "  run          - Run the API server"
	@echo "  clean        - Clean temporary files"
	@echo "  venv         - Create a virtual environment"
	@echo "  dev-install  - Install development dependencies"
	@echo "  format       - Format code with black and isort"
	@echo "  lint         - Lint code with flake8"
	@echo "  example      - Run example script (use AUDIO_FILE=path/to/audio.wav)"
	@echo "  help         - Show this help message" 
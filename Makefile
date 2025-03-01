.PHONY: setup install test run clean venv dev-install format lint example frontend-install frontend-start frontend-build run-all help

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

# Install frontend dependencies
frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Start frontend development server
frontend-start:
	@echo "Starting frontend development server..."
	cd frontend && NODE_OPTIONS=--openssl-legacy-provider npm start

# Build frontend for production
frontend-build:
	@echo "Building frontend for production..."
	cd frontend && npm run build

# Run both backend and frontend
run-all:
	@echo "Starting both backend and frontend..."
	chmod +x run.sh
	./run.sh

# Help
help:
	@echo "Available targets:"
	@echo "  setup           - Set up the project"
	@echo "  install         - Install dependencies"
	@echo "  test            - Run tests"
	@echo "  run             - Run the API server"
	@echo "  clean           - Clean temporary files"
	@echo "  venv            - Create a virtual environment"
	@echo "  dev-install     - Install development dependencies"
	@echo "  format          - Format code with black and isort"
	@echo "  lint            - Lint code with flake8"
	@echo "  example         - Run example script (use AUDIO_FILE=path/to/audio.wav)"
	@echo "  frontend-install - Install frontend dependencies"
	@echo "  frontend-start  - Start frontend development server"
	@echo "  frontend-build  - Build frontend for production"
	@echo "  run-all         - Run both backend and frontend"
	@echo "  help            - Show this help message" 

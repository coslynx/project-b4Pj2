# Define required variables
PYTHON := python3
PIP := pip3

# Default target
all: install

# Install dependencies
install: requirements.txt
	$(PIP) install -r requirements.txt

# Run the bot
run:
	$(PYTHON) src/main.py

# Format code with black
format:
	$(BLACK) src/

# Lint code with pylint
lint:
	$(PYLINT) src/

# Run tests (if applicable)
test:
	# Add your test commands here

# Clean up build artifacts
clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/

# Build Docker image
docker-build:
	docker-compose build

# Run Docker containers
docker-run:
	docker-compose up

# Stop Docker containers
docker-stop:
	docker-compose down

# Help target to show available commands
help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies"
	@echo "  make run           Run the bot"
	@echo "  make format        Format code with black"
	@echo "  make lint          Lint code with pylint"
	@echo "  make test          Run tests"
	@echo "  make clean         Clean up build artifacts"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-run   Run Docker containers"
	@echo "  make docker-stop  Stop Docker containers"

# Define phony targets
.PHONY: all install run format lint test clean docker-build docker-run docker-stop help
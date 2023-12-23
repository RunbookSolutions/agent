DOCKER_IMAGE_NAME := runbooksolutions/agent:latest

DOCKER_RUN := docker run -v $(PWD):/app

test:
	@echo "Running tests for $* package..."
	coverage run --source ./src/modules -m pytest tests
	coverage html
	coverage report --fail-under=80

.PHONY: run

run:
	@echo "Running the application..."
	@cd src && python main.py

.PHONY: clean

clean:
	@echo "Cleaning up..."
	@find . -name "*.pyc" -not -path "./OLD/*" -exec rm -f {} +
	@find . -name "__pycache__" -not -path "./OLD/*" -exec rm -rf {} +
	@find . -name ".pytest_cache" -not -path "./OLD/*" -exec rm -rf {} +
	@find . -name ".coverage" -not -path "./OLD/*" -exec rm -rf {} +
	@find . -name "htmlcov" -not -path "./OLD/*" -exec rm -rf {} +
	@find . -name "*.egg-info" -not -path "./OLD/*" -exec rm -rf {} +

docker:
	@echo "Building Docker image..."
	@docker build -t $(DOCKER_IMAGE_NAME) .

.PHONY: all

all: test run

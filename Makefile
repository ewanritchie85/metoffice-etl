################################################################################
#
# Makefile to build the project
#
################################################################################

PROJECT_NAME = metoffice-etl
PYTHON_INTERPRETER = python
SHELL := /bin/bash
PROFILE = default
PIP := pip
PYTHONPATH := $(shell pwd)/src
TEST_DIR := tests


## Create the Python virtual environment
create-environment:
	@echo ">>> Creating virtual environment in ./venv..."
	$(PYTHON_INTERPRETER) -m venv venv

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && PYTHONPATH=$(PYTHONPATH) $1
endef

requirements: create-environment ## Build the environment requirements
	$(call execute_in_env, $(PIP) install pip-tools)
	$(call execute_in_env, pip-compile requirements.in)
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################
# Set Up
bandit: ## Install bandit: finds common security issues in Python code.
	$(call execute_in_env, $(PIP) install bandit)

safety: ## Install safety: checks Python dependencies for known vulnerabilities.
	$(call execute_in_env, $(PIP) install safety)

black: ## Install black: formats code to follow PEP 8.
	$(call execute_in_env, $(PIP) install black)

coverage: ## Install coverage: measures code coverage.
	$(call execute_in_env, $(PIP) install coverage)

dev-setup: bandit safety black coverage ## Install Bandit, Black Coverage and Safety
	$(call execute_in_env, $(PIP) install -r requirements.txt)

# Build / Run

run-black: ## Run black to carry out PEP8  formatting
	$(call execute_in_env, black  ./src/*/*.py ./tests/*.py)

unit-test: ## Run unit tests using pytest
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest)

check-coverage: ## Run test coverage  check
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src ./tests/)
	
run-checks: run-black unit-test check-coverage ## Run Black, unit tests and coverage checks

build-lambda: ## build lambda zip file
	docker run --rm \
		--platform linux/amd64 \
		--entrypoint bash \
		-v "$$(pwd)":/var/task \
		-w /var/task \
		amazonlinux:2023 -c "\
			yum install -y gcc python3 python3-devel python3-pip zip && \
			pip3 install -r requirements.txt -t lambda_package && \
			cp -r src/* lambda_package/ && \
			cd lambda_package && zip -r ../lambda_package.zip ."
	rm -rf lambda_package

clean: ## Clean up environment and caches

	rm -rf venv __pycache__ .pytest_cache .mypy_cache .coverage

help: ## Show available make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	# awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

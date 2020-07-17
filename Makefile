# Makefile to simplify test and build.

.PHONY: all run test clean test-env lint style coverage

all: test

build-base:
	docker build -f Dockerfile.base -t monitorbot-base .

build: build-base
	docker build -f Dockerfile.code -t monitorbot-code .

run: build
	docker run -d \
	--env HOSTNAME=$(shell hostname) \
	--restart=always \
	-v /var/log:/code/logs monitorbot-code

build-python:
	python setup.py sdist bdist_wheel

clean:
	rm -rf coverage_html_report .coverage
	rm -rf monitorbot.egg-info
	rm -rf __pycache__
	rm -rf dist
	rm -rf build
	rm -rf venv-dev
	rm -rf .mypy_cache
	rm -rf .pytest_cache

test: lint style

lint:
	pylint monitorbot
	pytest --pylint --pylint-rcfile=.pylintrc --pylint-error-types=CWEF

style:
	flake8
	mypy monitorbot

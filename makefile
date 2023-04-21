SHELL:=/bin/bash -o pipefail
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
APP_NAME:=app
PYTHON:=python3.9

all: dependencies

fresh: clean dependencies

testenv: clean_testenv test_build
	docker compose up --build

testenv_d: clean_testenv test_build
	docker compose up --build -d

test:
	docker compose exec gpt4all-datalake pytest -svv --disable-warnings -p no:cacheprovider /app/tests

clean_testenv:
	docker compose down -v

fresh_testenv: clean_testenv testenv

venv:
	if [ ! -d $(ROOT_DIR)/env ]; then $(PYTHON) -m venv $(ROOT_DIR)/env; fi

dependencies: venv
	source $(ROOT_DIR)/env/bin/activate; yes w | python -m pip install -r $(ROOT_DIR)/api/requirements.txt

clean: clean_testenv
	# Remove existing environment
	rm -rf $(ROOT_DIR)/env;
	rm -rf $(ROOT_DIR)/api/$(APP_NAME)/*.pyc;

build:
	bash ./api/bin/build.sh gpt4all-datalake --tag $(DATE) dev

push:
	bash ./api/bin/push_ecr.sh gpt4all-datalake $(DATE) dev

test_build:
	DOCKER_BUILDKIT=1 docker build -t gpt4all-datalake --progress plain -f api/Dockerfile.buildkit .
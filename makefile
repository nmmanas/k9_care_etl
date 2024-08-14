install:
	venv/bin/pip install -Ur ./requirements.txt

unit-tests:
	pytest

build-docker-compose:
	sudo docker-compose build

run-docker-compose:
	sudo docker-compose --env-file .env.docker up

build-and-run-docker-compose: build-docker-compose run-docker-compose

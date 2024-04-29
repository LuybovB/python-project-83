PORT ?= 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$PORT page_analyzer:app

install:
	poetry install

build:
	poetry build

dev:
	poetry run flask run --port 8000

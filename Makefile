PORT ?= 8000

start:
	PYTHONPATH=$(pwd) poetry run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer.app:app

install:
	poetry install

build:
	poetry build

dev:
	poetry run flask run --port 8000

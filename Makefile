PORT ?= 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

build:
	poetry build

dev:
	poetry run flask --app page_analyzer:app run --port=8000
    poetry run python -m page_analyzer.app run --port 8000

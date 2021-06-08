install:
		python setup.py sdist install
update:
		twine upload dist/*
start:
		PYTHONPATH=.:src python hallmonitor/api.py
up:
		docker-compose build && docker-compose up
down:
		docker-compose -f docker-compose.yaml down

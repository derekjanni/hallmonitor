install:
		python setup.py install
up:
		docker-compose build && docker-compose up
down:
		docker-compose -f docker-compose.yaml down

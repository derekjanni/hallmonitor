install:
		rm -r dist && python setup.py sdist bdist_wheel install
update:
		twine upload dist/*
up:
		docker-compose build && docker-compose up
down:
		docker-compose -f docker-compose.yaml down

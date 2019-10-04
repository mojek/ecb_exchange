ENTER_DJANGO:=docker-compose exec web

enter:
	$(ENTER_DJANGO) sh

test:
	$(ENTER_DJANGO) python manage.py test

makemigrations:
	$(ENTER_DJANGO) python manage.py makemigrations

migrate:
	$(ENTER_DJANGO) python manage.py migrate

stop:
	docker-compose stop

kill:
	docker-compose down

start:
	docker-compose up

build:
	docker-compose up --build


	
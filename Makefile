.PHONY: up down build migrate test coverage collectstatic shell

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

test:
	docker-compose exec web pytest

coverage:
	docker-compose exec web pytest --cov=main --cov-report=term-missing

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

flush:
	docker-compose exec web python manage.py flush

shell:
	docker-compose exec web python manage.py shell
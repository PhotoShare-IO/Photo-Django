.PHONY: install-python
install-python:
	pyenv install 3.11

.PHONY: create-env
create-env: 
	pyenv virtualenv 3.11 photo-django

.PHONY: install-packages
install-packages:
	poetry install --without dev

.PHONY: install-dev-packages
install-dev-packages:
	poetry install --only dev

.PHONY: install-all-packages
install-all-packages:
	poetry install

.PHONY: run-server
run-server:
	python manage.py runserver 0.0.0.0:8000

.PHONY: create-admin
create-admin:
	python manage.py createsuperuser

.PHONY: make-migrations
make-migrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: load-fixtures
load-fixtures:
	python manage.py loaddata ./fixtures/*
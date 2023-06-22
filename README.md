# PhotoShare [Backend ⚙️]

----
## Table of Content
* **[Local Installing](#installing-python-311-via-pyenv-)**
  * [Installing Python version 3.11](#installing-python-version-311)
  * [Create Virtual Environment](#create-virtual-environment)
  * [Activate Virtual Environment](#activate-virtual-environment)
  * [Install Poetry](#install-poetry)
  * [Installing packages](#installing-packages)
* **[Managing Django](#managing-django)**
  * [Run Server](#run-server)
  * [Apply Migrations](#apply-migrations)
  * [Create New Migrations](#create-new-migrations)
  * [Create Admin](#create-admin)


## Installing Python 3.11 via pyenv 🐍

Firstly, install pyenv to your machine. Visit [official page](https://github.com/pyenv/pyenv#installation) and follow the instalation instructions.

#### Installing Python version 3.11

```sh
pyenv install 3.11
```

#### Create Virtual Environment

```sh
pyenv virtualenv 3.11 photo-django
```

#### Activate Virtual Environment

```sh
pyenv activate photo-django
```

#### Install Poetry

In activated `photo-django` virtual environment install poetry.

```sh
pip install poetry
```

#### Installing packages

For installing all packages (includes dev dependencies)

```sh
make install-all-packages
```

Installing packages for development

```
make install-packges
```

## Managing Django

#### Run Server

```sh
make run-server
```

#### Apply Migrations

```sh
make make-migrations
```

#### Create New Migrations

```sh
python manage.py makemigrations
```

#### Create Admin

```sh
make create-admin
```

# Trees Everywhere

- [Trees Everywhere](#trees-everywhere)
  - [Description](#description)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [Contributing](#contributing)

## Description

This is a project to make an API where one can create an user and plant trees, among other things. The main goal is to make a project using the following technologies:

- [x] [Python](https://www.python.org/)
- [x] [Poetry](https://python-poetry.org/)
- [x] [Django](https://www.djangoproject.com/)

## Installation

The project was made using Python 3.12 and Poetry. To install the project with all of it's dependencies, you can use the following commands:

```bash
poetry install
```

Before running the project, you need to create a `.env` file in the root of the project with the following content:

```env
# Database
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

> Using a `.env` file will only work in a development environment. In a production environment, you must use environment variables.

To run the project, you can use the following command:

<!-- TODO: ADD INFORMATION REGARDING ENVRIOMENT VARIABLES AND DATABASE BEFORE RUNNING THE PROJECT -->

```bash
poetry run python manage.py runserver
```

If wanted you can install only the production dependencies using the following command:

```bash
poetry install --no-dev
```

## Documentation

The documentation for the project without the exact project description can be found in the [docs](./docs) folder.

There, every analysis and thought process can be found. Aswell as any other documentation that is not directly related to the project conception.

## Contributing

If you want to contribute to the project, you can follow the [CONTRIBUTING.md](./CONTRIBUTING.md) file.

There, you can find the guidelines for contributing to the project.

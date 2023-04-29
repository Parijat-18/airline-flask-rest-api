# Airline Flask REST API

This repository contains a simple, yet comprehensive example of a RESTful API for a dummy airline management system. The API is built using Flask, a popular Python web framework, SQLAlchemy for database access, Flask-Smorest for API documentation, and Marshmallow for schema validation. The system allows you to manage users, flights, passengers, and seats in an organized and efficient manner. The API also supports authentication using JSON Web Tokens (JWT) to ensure secure access to its resources.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [API Usage](#api-usage)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## Features

- User management (registration, authentication, and authorization)
- Flight management (create, read, update, and delete flights)
- Passenger management (create, read, update, and delete passengers)
- Seat management (create, read, update, and delete seats)
- JWT-based authentication
- Alembic migrations for database schema management
- Marshmallow schema validation
- Flask-Smorest for API documentation
- Swagger-UI integration for interactive documentation

## Requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Alembic
- Marshmallow
- Flask-Smorest

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Parijat-18/airline-flask-rest-api.git
```

2. Create a virtual environment and install the required packages:

```bash
cd airline-flask-rest-api.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure the database URL in the `config.py` file.

4. Initialize the database and run the migrations:

```bash
flask db init
flask db upgrade
```

5. Run the application:

```bash
flask run
```

## API Usage

The API provides the following endpoints for managing resources:

- `/api/register`: Register a new user
- `/api/login`: Authenticate a user and generate a JWT
- `/api/flights`: Manage flights (GET, POST, PUT, DELETE)
- `/api/passengers`: Manage passengers (GET, POST, PUT, DELETE)
- `/api/seats`: Manage seats (GET, POST, PUT, DELETE)


## Database Schema

The database is designed with the following tables:

- `users`: Stores user information (id, first name, last name, email, password)
- `flights`: Stores flight information (id, PNR, origin, destination, flight time, basic fare)
- `passengers`: Stores passenger information (id, first name, last name, seat number, amount paid, PNR, user id)
- `seats`: Stores seat information (id, seat number, seat price, seat type, flight id, passenger id)
- `blocklist`: Stores JWT identifiers (id, jti) for revoked tokens

The relationships between tables are as follows:

- `users` 1:N `passengers`: Each user can have multiple passengers
- `flights` 1:N `seats`: Each flight can have multiple seats
- `passengers` 1:1 `seats`: Each passenger is assigned one seat

The database schema is designed to be extensible and maintainable, allowing for easy addition of new features or modifications to the existing data model.

## API Documentation

This API is fully documented using Flask-Smorest, which generates OpenAPI 3.0 specifications. We have also integrated Swagger-UI to provide interactive documentation for the API. You can access the interactive documentation at the following URL:

```
https://localhost:5000/swagger-ui/
```

This will allow you to explore the API's endpoints, parameters, and response formats in an easy-to-use interface.


## Contributing

If you would like to contribute to this project, please follow the usual GitHub fork and pull request workflow:

1. Fork the repository on GitHub
2. Clone your fork and create a new branch
3. Commit your changes to the new branch
4. Push the branch to your fork
5. Submit a pull request to the original repository

Please ensure that your changes are well-documented and follow the existing code style.

# Worklife Python Technical test

This project serves as a technical test for middle-senior backend developers in Python.

It makes use of FastAPI (and Pydantic), SQLAlchemy (orm), alembic (migrations).
It also uses PostgreSQL as database and poetry for dependency management.

## Overview

You are building an employee vacation handling system to manage leave.

Employees belong to teams. There can be many teams. One employee can belong to only one team.

An employee vacation has:
* A type
    * Unpaid leave
    * Paid leave
* A start date
* An end date

### Notes

For this project:
* There is no half-day leaves, only complete days.
* Employees work a typical work week of 5/7 with weekends being on Saturday-Sunday

## The project

You need to create an API to help manage vacations including:
* Models and relationships for the various entities
* Features logic
* API Endpoints

Your API should be able to handle the following features:
* Create employees
* Create, update and delete vacations
* Search for employees on vacation given various parameters
* When creating or updating a vacation, if there is an overlap or is contiguous to vacations of the same type, the vacation should be merged with the other ones


The current boilerplate should serve as a base to start with.
Feel free to upgrade / downgrade it as you see fit.


## What we expect

2 to 3 hours is a good target for this exercice, but you can spend as much or little time as you'd like.

Your answer to this test should be a repository.

Feel free to implement this project in whatever way you feel like, we do not impose any limitations/requirements, 
we simply give you a base to work with.

## Requirements

* docker
* poetry (optional, if you want to add libs)
* make (optional)

## Setup and usage

Create an empty `.env` file.

Depending on your docker and docker-compose setup you might need to use

`docker-compose up -d` or `docker compose up -d`

Once the container run, you should be able to access the docs at http://localhost:880/docs

To create and migrate the database with the migration already added:

You might need to create the database, in which case run `make create-db`

Then use `make migrate-db` to update the database schema.

If you make modifications/additions to models and want to auto generate migrations you can use. 
Don't forget to migrate the database afterwards using the command above.

`make autogenerate-migration revision_message='"your_message"'`

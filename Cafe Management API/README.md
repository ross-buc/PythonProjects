# Café Management API

This Flask API project is part of Angela Yu's "100 Days of Code" course. It allows users to manage cafés in a database by making GET, POST, PATCH, and DELETE requests. The project uses Flask, SQLAlchemy, RESTful principles, and JSON responses.

## Features

- Retrieve a random café from the database
- Get a list of all cafés in the database
- Add a new café to the database
- Update the coffee price of a café
- Delete a café from the database
- Search for cafés at a specific location


## Endpoints

- `GET /random` - Retrieve a random café from the database.
- `GET /all` - Get a list of all cafés in the database.
- `POST /add` - Add a new café to the database.
- `PATCH /update-price/<cafe_id>` - Update the coffee price of a café.
- `DELETE /report-closed/<cafe_id>` - Delete a café from the database.
- `GET /search?loc=<location>` - Search for cafés at a specific location.


## Credits

This project was inspired by Angela Yu's "100 Days of Code" course. You can find the course on [Udemy](https://www.udemy.com/course/100-days-of-code/).



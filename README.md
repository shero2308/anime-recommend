# Anime Recommendation System - API

This project provides a REST API for an Anime Recommendation System. It allows users to register, log in, search for anime, and receive personalized anime recommendations based on their preferences.

## Table of Contents
- [Project Setup](#project-setup)
- [Available Endpoints](#available-endpoints)
- [Sample Requests and Responses](#sample-requests-and-responses)

## Project Setup

Follow these steps to set up and run the project locally.

### 1. Clone the repository

git clone https://github.com/shero2308/anime-recommend

cd anime-recommend
### 2. Create a virtual environment
python3 -m venv env
source env/bin/activate   # On Windows, use `env\Scripts\activate`

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set up the database
Make sure you have PostgreSQL installed. Create a new database and update your settings.py file with the correct database credentials.
Run migrations to set up the database tables:
python manage.py migrate

### 5. Create a superuser (optional for admin access)
python manage.py createsuperuser

### 6. Run the development server
python manage.py runserver
Your API will now be running at http://127.0.0.1:8000/.

### Available Endpoints
Authentication:

POST /auth/register
Description: Register a new user.
Request Body:


{
  "username": "user1",
  "password": "password123"
}

Response:

{
  "message": "User created successfully!"
}

### POST /auth/login
Description: Log in and retrieve JWT tokens.

Request Body:

{
  "username": "user1",
  "password": "password123"
}

Response:

{
  "refresh": "refresh_token",
  "access": "access_token"
}

### Anime Search
GET /anime/search
Description: Search for anime by name or genre.
Query Parameters:

name: (Optional) The name of the anime.
genre: (Optional) The genre of the anime.

Example Request:

GET /anime/search?name=Naruto&genre=Action

Response:

[
  {
    "id": 1,
    "title": {
      "romaji": "Naruto"
    },
    "genres": ["Action", "Adventure", "Fantasy"],
    "popularity": 1000000
  }
]

### Anime Recommendations

GET /anime/recommendations

Description: Fetch anime recommendations based on the authenticated user's preferences.
Authentication: This endpoint requires the user to be authenticated with a JWT token.
Response:

[
  {
    "id": 2,
    "title": {
      "romaji": "Naruto Shippuden"
    },
    "genres": ["Action", "Adventure", "Shonen"],
    "popularity": 950000
  }
]

### Manage User Preferences
GET /user/preferences
Description: Retrieve the preferences of the authenticated user.

Response:

{
  "genres": ["Action", "Adventure"]
}
POST /user/preferences
Description: Update the preferences of the authenticated user.

Request Body:

{
  "genres": ["Action", "Adventure", "Fantasy"]
}

Response:

{
  "message": "Preferences updated successfully!"
}

Sample Requests and Responses

### 1. Register a New User

Request:

POST /auth/register
Content-Type: application/json
{
  "username": "user1",
  "password": "password123"
}

Response:

{
  "message": "User created successfully!"
}

### 2. Log in

Request:

POST /auth/login
Content-Type: application/json
{
  "username": "user1",
  "password": "password123"
}

Response:


{
  "refresh": "refresh_token",
  "access": "access_token"
}

### 3. Search for Anime

Request:

GET /anime/search?name=Naruto&genre=Action

Response:

[
  {
    "id": 1,
    "title": {
      "romaji": "Naruto"
    },
    "genres": ["Action", "Adventure", "Fantasy"],
    "popularity": 1000000
  }
]

### 4. Get Recommendations
Request:

GET /anime/recommendations
Authorization: Bearer access_token

Response:

[
  {
    "id": 2,
    "title": {
      "romaji": "Naruto Shippuden"
    },
    "genres": ["Action", "Adventure", "Shonen"],
    "popularity": 950000
  }
]

### Troubleshooting
If you encounter any issues, ensure that all dependencies are installed using pip install -r requirements.txt.
Make sure the database is set up correctly and migrations are applied (python manage.py migrate).
Check your Django server logs for any errors when interacting with the API.
Feel free to modify or extend the endpoints as necessary. Enjoy building your Anime Recommendation System!







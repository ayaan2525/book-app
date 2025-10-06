# Book Recommendation System API

A minimal backend for a Book Recommendation System built with FastAPI, SQLAlchemy, and Pydantic.
It provides JWT-based user authentication, book listing with dynamically calculated average ratings, and user reviews.

## Table of Contents

- [Architecture](#architecture)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Design Rationale](#design-rationale)


## Architecture
The application follows a **3-layered architecture** to separate concerns:

- **API Layer (main.py)**: Handles HTTP requests, and input/output validation with Pydantic.
  
- **Service Layer (services.py)**: Contains the core business logic, computes average ratings, applies filters, and orchestrates repository calls..
  
- **Repository Layer (repository.py)**: Manages all direct database interactions using SQLAlchemy ORM.

This structure is held together by FastAPI's dependency injection system, which makes the components decoupled and easily testable.

**Data flow (overview):**
Client -> API (router + schemas)
-> Service (business rules, validation)
-> Repository (SQLAlchemy session)
-> Database (SQLite by default)


---

## Requirements

- Python **3.11**
- pip / venv
- SQLite (bundled with Python)

---

## Setup

Create and activate a virtual environment, then install dependencies.

```bash
python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```


## Configuration

Copy the example environment file and update if necessary (defaults are fine for local use).
```bash
cp .env.example .env
```

## Running the App
From the project root:

  ```bash
  uvicorn main:app --reload
```
You can access the interactive API documentation at http://127.0.0.1:8000/docs.

## API Endpoints

**Auth**

**POST** */login*

Exchange username/password for a JWT access token.

Request:
{ "username": "mark", "password": "mark123" }

Response:
{ "access_token": "<JWT>", "token_type": "bearer" }

**Books**

GET */books*

List books with fields id, title, author, genre, and dynamically computed average_rating.

Query params:
- q (optional) — search by title/author

GET */books/{book_id}/reviews*
Return all reviews for a book.

**Reviews**

POST */books/{book_id}/reviews*

Create or update the authenticated user’s review for a book.

Request body:

{
  "rating": 5,
  "review_text": "Loved the world-building."
}

## Testing
The service layer is unit-tested using pytest, with repositories mocked to ensure isolation.
```bash
pytest -v
```

# Design Rationale
Layered architecture: Keeps business logic out of routes and DB code; simplifies testing.

Dependency injection: The design uses dependency injection so the app can use real or mock repositories interchangeably.

JWT auth: Stateless sessions; easy to protect routes.

SQLite by default: Zero external dependencies.

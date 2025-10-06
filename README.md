**Book Recommendation System API**

This project is a simple Book Recommendation System backend built with FastAPI.

It provides a RESTful API for user authentication, listing books with dynamically calculated average ratings, and managing book reviews.

**Architecture**
The application follows a 3-layered architecture to separate concerns:

  **API Layer (main.py)**: Handles HTTP requests, data validation via Pydantic, and user-facing responses.
  
  **Service Layer (services.py)**: Contains the core business logic.
  
  **Repository Layer (repository.py)**: Manages all direct database interactions using SQLAlchemy.

This structure is held together by FastAPI's dependency injection system, which makes the components decoupled and easily testable.

**Setup and Run**
This project uses Python 3.11 and SQLite, requiring no external database services.

**1. Create a Virtual Environment**:

  *python3 -m venv venv*
  *source venv/bin/activate*

**2. Install Dependencies**:
  
  *pip install -r requirements.txt*

**3. Configure Environment**:
Copy the example environment file and update if necessary (defaults are fine for local use).

  *cp .env.example .env*

**4. Run the Application**:
To start the server,
  
  *uvicorn main:app --reload*

You can access the interactive API documentation at http://127.0.0.1:8000/docs.

**How to Run Tests**
The service layer is unit-tested using pytest, with repositories mocked to ensure isolation.

**2. Run Pytest**:

  *python -m pytest*

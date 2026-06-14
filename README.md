# MyAPI

A FastAPI backend with JWT authentication, SQLite database, ownership-based access control, automated tests, and Docker support.

![CI](https://github.com/pratikbyte8102/myapi/actions/workflows/ci.yml/badge.svg)

## Features

- CRUD operations for items
- User registration & login (JWT authentication)
- Item ownership (users can only edit/delete their own items)
- SQLite database (via SQLModel)
- Automated tests with pytest
- Dockerized for easy deployment

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- JWT (python-jose)
- pytest

## Run with Docker (recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running

### Steps

1. Clone the repository
```bash
   git clone https://github.com/pratikbyte8102/myapi.git
   cd myapi
```

2. Create your `.env` file (copy from example, then edit `SECRET_KEY`)
```bash
   copy .env.example .env
```

3. Build the Docker image
```bash
   docker build -t myapi .
```

4. Run the container
```bash
   docker run -d -p 8000:8000 --env-file .env --name myapi-container myapi
```

5. Open the API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Useful Docker commands

```bash
docker ps
docker logs myapi-container
docker stop myapi-container
docker start myapi-container
docker rm myapi-container
```

## Run locally (without Docker)

1. Create virtual environment
```bash
   python -m venv venv
```

2. Activate it
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Set up environment variables
```bash
   copy .env.example .env
```

5. Run the server
```bash
   uvicorn main:app --reload
```

6. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running Tests

```bash
pytest -v
```

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login, returns JWT token | No |

### Items
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/items` | List all items | No |
| GET | `/items/{id}` | Get a single item | No |
| POST | `/items` | Create a new item | Yes |
| PUT | `/items/{id}` | Update an item (owner only) | Yes |
| DELETE | `/items/{id}` | Delete an item (owner only) | Yes |
| GET | `/items/me/my-items` | Get items owned by current user | Yes |

## Authentication

1. Register a user via `/auth/register`
2. Login via `/auth/login` to receive a JWT token
3. Use the token in the `Authorization: Bearer <token>` header for protected routes
   - In Swagger UI, click the **Authorize** button and enter your credentials
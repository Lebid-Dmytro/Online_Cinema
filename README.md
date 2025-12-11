# Online Cinema

Online Cinema Platform - a digital platform for watching and purchasing movies.

## Setup

1. Clone the repository and install dependencies:
```bash
git clone <https://github.com/Lebid-Dmytro/Online_Cinema.git>
cd Online_Cinema
poetry install
```

2. Start services with Docker Compose:
```bash
docker-compose up -d
```

3. Start the application:
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation (Swagger) at `http://localhost:8000/docs`

## Authentication Endpoints

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/auth/change-password` - Change password (requires authentication)
- `GET /api/v1/auth/me` - Get current user info (requires authentication)

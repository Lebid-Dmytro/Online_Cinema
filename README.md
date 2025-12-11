# Online Cinema

Online Cinema Platform - a digital platform for watching and purchasing movies.

## Project Structure

```
Online_Cinema/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configuration and utilities
│   ├── models/        # Database models
│   └── schemas/       # Pydantic schemas
├── alembic/           # Database migrations
├── docker-compose.yml # Docker services configuration
└── pyproject.toml     # Poetry dependencies

```

## Setup

### Prerequisites

- Python 3.11+
- Poetry
- Docker and Docker Compose
- PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Online_Cinema
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start services with Docker Compose:
```bash
docker-compose up -d
```

5. Run database migrations:
```bash
poetry run alembic upgrade head
```

6. Start the application:
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation (Swagger) at `http://localhost:8000/docs`

## Authentication

### Endpoints

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `POST /api/v1/auth/logout` - Logout (revoke token)
- `POST /api/v1/auth/change-password` - Change password (requires authentication)
- `GET /api/v1/auth/me` - Get current user info (requires authentication)

### User Groups

- **USER**: Basic user with access to catalog and user interface
- **MODERATOR**: Can manage movies, view sales, etc.
- **ADMIN**: Full access, can manage users and groups

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Quality

```bash
poetry run black .
poetry run flake8 .
poetry run mypy .
```

## Branches

- `main` - Main development branch
- `auth` - Authentication feature branch

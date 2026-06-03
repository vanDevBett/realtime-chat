# Realtime Chat API

Realtime chat API built with FastAPI, WebSockets and Redis pub/sub.

## Tech Stack

- **FastAPI** — Python web framework
- **WebSockets** — Realtime bidirectional communication
- **Redis** — Pub/sub message broker
- **PostgreSQL** — Message persistence
- **SQLAlchemy** — ORM
- **bcrypt** — Password hashing
- **python-jose** — JWT tokens
- **Docker** — Containerization
- **pytest** — Testing

## Features

- JWT authentication
- Realtime messaging with WebSockets
- Multiple chat rooms
- Message persistence in PostgreSQL
- Redis pub/sub for message broadcasting

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.12+

### Run the project

```bash
# Clone the repository
git clone git@github.com:vanDevBett/realtime-chat.git
cd task-manager-api
```

```bash
# Create the environment file
cp .env.example .env
```

```bash
# Create and activate virtual environment

# Mac / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

```bash
# Start the containers
docker compose up --build
```

API available at `http://localhost:8000`

Interactive documentation at `http://localhost:8000/docs`

### Test the chat

Open `test_chat.html` in two browser tabs, register two users, paste their tokens and start chatting in realtime.

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /auth/register | Register a new user | No |
| POST | /auth/login | Login and get JWT token | No |

### Chat
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /chat/rooms/{room}/messages | Get room message history | No |
| WS | /chat/ws/{room}?token=xxx | Connect to a chat room | JWT |

## WebSocket Usage

```javascript
const ws = new WebSocket('ws://localhost:8000/chat/ws/general?token=YOUR_JWT');

ws.onmessage = (e) => {
    const message = JSON.parse(e.data);
    console.log(`${message.full_name}: ${message.content}`);
};

ws.send(JSON.stringify({ content: "Hello world" }));
```

## Run Tests

```bash
pytest tests/ -v
```

## Project Structure

```
app/
├── api/          # Endpoints and WebSocket handlers
├── core/         # Config, database, security, dependencies
├── models/       # Database models
├── schemas/      # Pydantic schemas
├── services/     # Business logic, Redis and chat services
└── main.py       # Entry point
```

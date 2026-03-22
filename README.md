# CipherForge - Backend

FAST API For CipherForge. Built With FastAPI.

## How It Works

You Send A Request With Your Preferences (Length, Character Types), And It Gives You Back A Secure Random Password.

## Setup

1. Install Dependencies:

```bash
pip install -r requirements.txt
```

2. Run The Server:

```bash
uvicorn App:app --reload --port 8000
```

Server Starts At `http://localhost:8000`.

## API

**`GET /`** — Check If The Server Is Running.

**`POST /generate`** — Generate A Single Password.

**`POST /generate-bulk`** — Generate Multiple Passwords At Once (Pass A `count` Field).

Request Body For Both:

```json
{
  "length": 16,
  "include_uppercase": true,
  "include_lowercase": true,
  "include_digits": true,
  "include_special": true
}
```

## Project Structure

```
Backend/
├── App.py                    — Routes And Server Setup
├── Tool/
│   └── GeneratePassword.py   — Password Generation Logic
├── .env                      — Environment Config
├── requirements.txt          — Dependencies
└── .gitignore
```

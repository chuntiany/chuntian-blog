# ChunTian's Blog System

A modern, full-stack blog application built with Python Flask and Vue.js 3.

## Project Overview

This project is a personal blog system featuring a clean, minimalist UI, Markdown support, and a comprehensive admin dashboard.

### Tech Stack

- **Backend**: Python 3.12, Flask, SQLAlchemy, MySQL
- **Frontend**: Vue.js 3, Vite, Pinia, Vue Router
- **Database**: MySQL 8.0+
- **Styling**: Custom CSS with a modern design system

## Project Structure

```
blog/
├── backend/            # Flask application
│   ├── app.py          # Application factory
│   ├── config.py       # Configuration settings
│   ├── extensions.py   # Flask extensions (DB, Migrate, Login, CORS)
│   ├── models.py       # Database models
│   └── routes/         # API endpoints
├── frontend/           # Vue.js application
│   ├── src/
│   │   ├── views/      # Page components (Home, Article, Admin)
│   │   ├── stores/     # Pinia state management
│   │   └── style.css   # Global styles
│   └── vite.config.js  # Vite configuration
├── tests/              # Backend tests
├── claude.md           # Development guidelines
├── progress.md         # Project status tracking
├── phase.md            # Phase planning and architecture
└── task.md             # Detailed task checklist
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- MySQL Server

### Backend Setup

1.  Navigate to the backend directory (or root):
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure the database in `config.py` or `.env`.
5.  Initialize the database:
    ```bash
    flask db upgrade
    # Or use the helper script
    python create_db.py
    ```
6.  Run the server:
    ```bash
    flask run
    ```

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## Features

- **Public Interface**:
    - Modern, responsive homepage with sidebar navigation.
    - Article detail page with Markdown rendering and auto-generated Table of Contents.
    - User login and registration.
- **Admin Dashboard**:
    - Secure admin authentication.
    - Article management (Create, Edit, Delete) with Markdown editor.
    - Category and Comment management.
    - System settings configuration.

## Documentation

- `progress.md`: Check current progress and next steps.
- `phase.md`: Architecture design and phase planning.
- `claude.md`: Coding conventions and guidelines.

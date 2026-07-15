# Trekking Management System

A comprehensive web application designed for managing trekking activities, built with a modern architecture featuring a Vue 3 frontend and a Flask backend.

## Tech Stack

### Frontend
- **Vue 3**: Reactive user interface
- **Vite**: Fast frontend build tool
- **Pinia**: State management
- **Vue Router**: Client-side routing
- **Axios**: HTTP client for API requests
- **Bootstrap 5**: CSS framework for styling

### Backend
- **Flask**: Lightweight Python web framework
- **Flask-SQLAlchemy**: ORM for database interactions
- **Flask-JWT-Extended**: Authentication using JSON Web Tokens
- **Celery & Redis**: Asynchronous task queue and message broker
- **Flask-Caching**: Caching mechanisms for improved performance
- **Flask-Mail**: Email integration

## Project Structure

- `frontend/`: Contains the Vue 3 application.
- `backend/`: Contains the Flask server, models, routes, and Celery tasks.

## Setup Instructions

### Backend Setup
1. Navigate to the `backend` directory: 
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure **Redis** is installed and running on your system, as it is required for Celery and caching.
5. Set up the database and run the Flask application. You can use the provided script or start it manually:
   ```bash
   python app.py
   ```
6. Start the Celery worker (in a separate terminal inside the `backend` directory):
   ```bash
   celery -A celery_utils.celery worker --loglevel=info
   ```

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the provided local URL in your browser to view the app.
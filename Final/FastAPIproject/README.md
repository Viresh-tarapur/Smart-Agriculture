# Plant Disease Detection System (FastAPI)

This project is a FastAPI-based application for detecting plant diseases. It includes a dashboard, specialized monitoring pages, and integration with various APIs.

## Prerequisites

- Python 3.8+
- [Optional] Virtual Environment (venv)

## Installation

1. **Clone the repository** (if not already done).
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Application

There are two ways to start the server:

### Option 1: Run via Python Script (Recommended)
```powershell
python run_fastapi.py
```

### Option 2: Run via Batch File
Double-click `run.bat` or run it from the terminal:
```powershell
.\run.bat
```

## Accessing the App

Once started, the server will be live at:
**[http://localhost:5000](http://localhost:5000)**

## Project Structure

- `main.py`: Application entry point and router setup.
- `run_fastapi.py`: Helper script to launch the uvicorn server with hot reloading.
- `routes/`: Contains different API and page routers (`auth`, `gps`, `pages`).
- `templates/`: HTML templates for the frontend.
- `static/`: Static assets like CSS, images, and JavaScript.
- `database.py`/`models.py`: Database configuration and ORM models.
- `requirements.txt`: List of Python dependencies.

## Key Features
- **Disease Monitor**: Track and predict plant diseases.
- **GPS Integration**: Real-time location tracking for bins/sensors.
- **Authentication**: Secure login and registration system.
- **Marketplace Dashboard**: Access agri-related products and information.

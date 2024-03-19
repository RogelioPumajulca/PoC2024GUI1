# PoC 2024 - GUI

A web-based graphical user interface (GUI) for the PoC 2024 

#### Authors
Bergen Davis, Rogelio Pumajulca, Jainil Shah

## Directory Structure
- `frontend`: Vue.js frontend code, static files
- `backend`: Python Flask backend



## How to use
Start the backend, the frontend starts automatically.
```
cd backend
python app.py
```

Go to (http://localhost:8000)[http://localhost:8000]

### Prerequisites
For backend:
```
pip install -r ./backend/requirements.txt
```



## Notes
The frontend is made with Vue.js Options API and in HTML. It uses AJAX/Jquery to make polling request to the backend and update on changes.
The backend is Flask app that both serves the static files and implements the API for the different modules. It uses multithreading to run the different modules and communicate with them.

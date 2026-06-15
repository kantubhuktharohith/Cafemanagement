# Cafemanagement

Cafemanagement is a minimal cafe/point-of-sale management web application built with Python. It provides a simple interface for staff to log in, create and manage receipts, and view a dashboard of recent activity. The project is intended as a lightweight starter app for small cafes or for learning Flask web development.

**Features**
- User login and session flow
- Dashboard view with recent receipts
- Create, store, and list receipts (saved to local database)
- Simple HTML templates and CSS in `templates/` and `static/`

**Tech stack**
- Python 3.10+ (or compatible)
- Flask (routes and templating)
- SQLite or file-based storage (see `database.py`)

**Getting started**

Prerequisites
- Python 3.10 or newer
- pip

Install dependencies

```bash
python -m pip install -r requirements.txt
```

Running the app (development)

```bash
python app.py
# then open http://127.0.0.1:5000 in your browser
```

Project layout

- `app.py` - application entrypoint and route definitions
- `database.py` - database helpers and schema functions
- `utils.py` - utility helpers used by the app
- `templates/` - Jinja2 HTML templates (`base.html`, `login.html`, `dashboard.html`)
- `static/` - static assets (CSS, JS)
- `receipts/` - stored receipt files or exports
- `requirements.txt` - Python dependencies

Usage notes
- The app includes a basic login form (see `templates/login.html`). For local testing, credentials or user setup may be implemented in `app.py` or `database.py` depending on the project code.
- Receipts are saved under the `receipts/` folder; review `app.py` to see how receipts are created and formatted.

Contributing
- Feel free to open issues or submit pull requests to add features, tests, or harden authentication.

License
- This repository does not include a license file by default. Add a `LICENSE` if you intend to open-source this project.

Contact
- For questions or help, inspect the source files (`app.py`, `database.py`, `utils.py`) or reach out to the project owner.

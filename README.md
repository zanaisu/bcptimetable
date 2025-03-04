# A-Level Study Tracker

A web application to help manage and track A-level studies for OCR A Chemistry, OCR A Biology, and AQA Psychology.

## Features

- User authentication system
- Daily task generation based on curriculum
- Task management (complete or swap tasks)
- Topic confidence tracking
- Weekend mode for flexible study sessions
- Curriculum browser with confidence adjustment
- Progress tracking and statistics
- Exam calendar with scheduled tasks
- Dark mode support

## Setup Instructions

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bcptimetable.git
cd bcptimetable
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python -m app.init_db
```

5. Run the application:
```bash
flask run
```

The application will be available at http://127.0.0.1:5000/

### Railway Deployment

1. Create a new project on Railway.app
2. Connect your GitHub repository
3. Add a PostgreSQL database service
4. Set environment variables:
   - `SECRET_KEY`: A secure random string
   - `DATABASE_URL`: Will be automatically set by Railway

5. Deploy the application
6. Run database initialization commands:
```bash
flask db upgrade
python -m app.init_db
```

## Technology Stack

- Backend: Flask (Python)
- Database: SQLAlchemy with SQLite (development) / PostgreSQL (production)
- Frontend: HTML, CSS, JavaScript
- CSS Framework: Bootstrap 5
- Icons: Font Awesome
- Deployment: Railway.app

## License

This project is licensed under the MIT License.
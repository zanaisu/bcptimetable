# BCP Timetable

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
git clone https://github.com/zanaisu/bcptimetable.git
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
4. Use the `.env.railway` file for deployment:
   - Rename `.env.railway` to `.env` before deploying to Railway
   - Or set the environment variables manually in the Railway dashboard

5. Deploy the application
6. Run database initialization commands through the Railway CLI or web interface:
```bash
python run.py init-db
```

Note: Railway will automatically set up the PostgreSQL environment variables for you, but the `.env.railway` file contains all the necessary configuration for reference.

### Switching Between Local and Railway Environments

This project includes two environment configuration files:
- `.env.local` - For local development with SQLite
- `.env.railway` - For Railway deployment with PostgreSQL

To switch between environments, you can use the provided script:
```bash
# Switch to local development environment
switch_env.bat local

# Switch to Railway deployment environment
switch_env.bat railway
```

The script will copy the appropriate .env file to the main .env file used by the application.

## Technology Stack

- Backend: Flask (Python)
- Database: SQLAlchemy with SQLite (development) / PostgreSQL (production)
- Frontend: HTML, CSS, JavaScript
- CSS Framework: Bootstrap 5
- Icons: Font Awesome
- Deployment: Railway.app

## License

This project is licensed under the MIT License.#   b c p t i m e t a b l e 
 

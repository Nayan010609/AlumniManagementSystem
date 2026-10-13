https://alumnimanagementsystem.onrender.com
# Alumni Mentoring & Engagement Management System

A comprehensive full-stack Python web application for managing alumni mentoring programs, engagement, and donations.

## Features

✨ **Core Functionality:**
- **Alumni Registration** - Register alumni with unique email constraints
- **Mentoring Requests** - Students can request mentoring from alumni
- **Mentor Assignment** - Assign alumni mentors to student requests (3NF database design)
- **Donation Tracking** - Record and manage alumni donations with amount validation
- **Events Management** - Manage alumni events with capacity tracking
- **Reports & Views** - View mentor matches, donation summaries, and event details

🔒 **Database Constraints:**
- Unique email constraints for alumni records
- Positive amount validation for donations
- One active mentor per mentoring request
- Proper relational database schema (3NF)

## Tech Stack

- **Backend:** Python with Flask framework
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Server:** Flask development server

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nayan010609/AlumniManagementSystem.git
   cd AlumniManagementSystem
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Access the application:**
   - Open your browser and navigate to: `http://127.0.0.1:5000`
   - The application will be fully functional with sample data pre-loaded

## Project Structure

```
AlumniManagementSystem/
├── app.py                 # Main Flask application with database models and routes
├── templates/
│   └── index.html        # Web interface (frontend)
├── requirements.txt      # Python dependencies
├── alumni.db            # SQLite database file
├── tests/
│   ├── __init__.html    # Original HTML file (reference)
│   └── __init__.py
└── README.md            # This file
```

## API Endpoints

### Data Management
- `GET /` - Serve the web interface
- `GET /api/data` - Get all data (alumni, students, requests, donations, events)

### Alumni Operations
- `POST /api/alumni/register` - Register a new alumni member

### Mentoring
- `POST /api/mentoring/request` - Submit a student mentoring request
- `POST /api/mentoring/assign` - Assign a mentor to a request

### Donations
- `POST /api/donation/record` - Record a new donation

## Database Schema

### Alumni Table
- `id` - Primary Key
- `name` - Alumni full name
- `email` - Unique email address
- `year` - Graduation year
- `prog` - Programme/Degree

### Student Table
- `id` - Primary Key
- `name` - Student name
- `email` - Student email

### MentoringRequest Table
- `id` - Primary Key
- `student_id` - Foreign Key (Student)
- `topic` - Mentoring topic
- `status` - Request status (Pending/Assigned)
- `alumni_id` - Foreign Key (Alumni mentor)

### Donation Table
- `id` - Primary Key
- `alumni_id` - Foreign Key (Alumni)
- `amount` - Donation amount (must be > 0)
- `date` - Donation date

### Event Table
- `id` - Primary Key
- `name` - Event name
- `date` - Event date
- `capacity` - Event capacity

## Sample Data

The application comes pre-loaded with sample data:

**Alumni:**
- Alice Smith (B.Tech Computer Science, 2020)
- Bob Jones (B.Sc Physics, 2018)

**Students:**
- David Miller
- Eva Green

**Sample Mentoring Requests:**
- Software Engineering Career Guidance (Assigned to Alice)
- Higher Studies in Physics (Pending)

**Sample Donations:**
- Alice Smith: $500.00
- Bob Jones: $250.50

**Events:**
- Annual Alumni Meet 2026 (Capacity: 100)
- Tech Career Fair (Capacity: 50)

## Usage Guide

### Register Alumni
1. Click on "Register Alumni" tab
2. Fill in name, email, graduation year, and programme
3. Click "Save Alumni"

### Submit Mentoring Request
1. Click on "Mentoring Request" tab
2. Enter student name, email, and topic
3. Click "Submit Request"

### Assign a Mentor
1. Click on "Assign Mentor (3NF)" tab
2. Select a pending request from the dropdown
3. Select a mentor (alumni) from the dropdown
4. Click "Confirm Assignment"

### Record a Donation
1. Click on "Donations" tab
2. Select an alumni donor
3. Enter donation amount (must be positive)
4. Select donation date
5. Click "Record Donation"

### View Reports
1. Click on "Reports & Views" tab
2. View three main reports:
   - Mentor Matches & Requests (JOIN data)
   - Alumni Donations Summary
   - Events & Capacity Status

## Database Constraints & Validation

- **Email Uniqueness:** Alumni email addresses must be unique
- **Donation Amount:** Must be greater than 0
- **Mentor Assignment:** Only one active mentor per request
- **Data Integrity:** Foreign key relationships enforced by SQLAlchemy

## Development

### Database Initialization
The application automatically initializes the database with sample data on first run. The database file (`alumni.db`) is created in the project root directory.

### Modifying the Database
To reset the database and reload sample data:
1. Delete the `alumni.db` file
2. Restart the application: `python app.py`

## Requirements

See `requirements.txt` for detailed dependencies:
- Flask 3.1.0
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.1.0

## Future Enhancements

- User authentication and authorization
- Email notifications for mentoring requests
- Advanced search and filtering
- Export reports to PDF/Excel
- Alumni directory with search functionality
- Event RSVP system
- Integration with third-party payment systems for donations

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please reach out to the project maintainers at the GitHub repository: https://github.com/Nayan010609/AlumniManagementSystem

---

**Created:** October 2026  
**Status:** Active Development

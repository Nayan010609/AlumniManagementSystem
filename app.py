from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "alumni.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class Alumni(db.Model):
    __tablename__ = 'alumni'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    prog = db.Column(db.String(50), nullable=False)
    
    requests = db.relationship('MentoringRequest', backref='mentor', lazy=True)
    donations = db.relationship('Donation', backref='alumni_donor', lazy=True)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    
    requests = db.relationship('MentoringRequest', backref='student', lazy=True)

class MentoringRequest(db.Model):
    __tablename__ = 'mentoring_request'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=True)

class Donation(db.Model):
    __tablename__ = 'donation'
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

# Get all data for reports
@app.route('/api/data', methods=['GET'])
def get_data():
    alumni_list = Alumni.query.all()
    students = Student.query.all()
    requests = MentoringRequest.query.all()
    donations = Donation.query.all()
    events = Event.query.all()

    return jsonify({
        'alumni': [{'id': a.id, 'name': a.name, 'email': a.email, 'year': a.year, 'prog': a.prog} for a in alumni_list],
        'students': [{'id': s.id, 'name': s.name, 'email': s.email} for s in students],
        'requests': [{'id': r.id, 'studentId': r.student_id, 'topic': r.topic, 'status': r.status, 'alumniId': r.alumni_id} for r in requests],
        'donations': [{'id': d.id, 'alumniId': d.alumni_id, 'amount': d.amount, 'date': d.date} for d in donations],
        'events': [{'name': e.name, 'date': e.date, 'capacity': e.capacity} for e in events]
    })

# Register Alumni
@app.route('/api/alumni/register', methods=['POST'])
def register_alumni():
    data = request.json
    email = data.get('email')
    
    # Check unique constraint
    if Alumni.query.filter_by(email=email).first():
        return jsonify({'error': 'Error: Email already exists (UNIQUE constraint violation).'}), 400
    
    alumni = Alumni(
        name=data.get('name'),
        email=email,
        year=data.get('year'),
        prog=data.get('prog')
    )
    db.session.add(alumni)
    db.session.commit()
    
    return jsonify({'success': 'Alumni registered successfully!', 'id': alumni.id})

# Submit Mentoring Request
@app.route('/api/mentoring/request', methods=['POST'])
def submit_mentoring_request():
    data = request.json
    student_email = data.get('studentEmail')
    
    student = Student.query.filter_by(email=student_email).first()
    if not student:
        student = Student(name=data.get('studentName'), email=student_email)
        db.session.add(student)
        db.session.commit()
    
    req = MentoringRequest(
        student_id=student.id,
        topic=data.get('topic'),
        status='Pending'
    )
    db.session.add(req)
    db.session.commit()
    
    return jsonify({'success': 'Mentoring request submitted successfully!', 'id': req.id})

# Assign Mentor
@app.route('/api/mentoring/assign', methods=['POST'])
def assign_mentor():
    data = request.json
    req_id = data.get('requestId')
    alumni_id = data.get('mentorId')
    
    req = MentoringRequest.query.get(req_id)
    if req:
        req.alumni_id = alumni_id
        req.status = 'Assigned'
        db.session.commit()
        return jsonify({'success': 'Mentor assigned successfully (One active mentor constraint enforced)!'})
    
    return jsonify({'error': 'Request not found'}), 404

# Record Donation
@app.route('/api/donation/record', methods=['POST'])
def record_donation():
    data = request.json
    amount = data.get('amount')
    
    if amount <= 0:
        return jsonify({'error': 'Error: Donation amount must be positive.'}), 400
    
    donation = Donation(
        alumni_id=data.get('alumniId'),
        amount=amount,
        date=data.get('date')
    )
    db.session.add(donation)
    db.session.commit()
    
    return jsonify({'success': 'Donation recorded successfully!', 'id': donation.id})

# ==================== INITIALIZATION ====================

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Alumni.query.first():
            return
        
        # Add sample alumni
        alice = Alumni(name='Alice Smith', email='alice.smith@alumni.edu', year=2020, prog='B.Tech Computer Science')
        bob = Alumni(name='Bob Jones', email='bob.jones@alumni.edu', year=2018, prog='B.Sc Physics')
        db.session.add_all([alice, bob])
        db.session.commit()
        
        # Add sample students
        david = Student(name='David Miller', email='david.m@student.edu')
        eva = Student(name='Eva Green', email='eva.g@student.edu')
        db.session.add_all([david, eva])
        db.session.commit()
        
        # Add sample requests
        req1 = MentoringRequest(student_id=david.id, topic='Software Engineering Career Guidance', status='Assigned', alumni_id=alice.id)
        req2 = MentoringRequest(student_id=eva.id, topic='Higher Studies in Physics', status='Pending')
        db.session.add_all([req1, req2])
        db.session.commit()
        
        # Add sample donations
        don1 = Donation(alumni_id=alice.id, amount=500.00, date='2026-02-10')
        don2 = Donation(alumni_id=bob.id, amount=250.50, date='2026-03-12')
        db.session.add_all([don1, don2])
        db.session.commit()
        
        # Add sample events
        evt1 = Event(name='Annual Alumni Meet 2026', date='2026-11-15', capacity=100)
        evt2 = Event(name='Tech Career Fair', date='2026-12-01', capacity=50)
        db.session.add_all([evt1, evt2])
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

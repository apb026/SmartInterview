from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resumes = db.relationship('Resume', backref='user', lazy=True)
    job_descriptions = db.relationship('JobDescription', backref='user', lazy=True)
    interviews = db.relationship('Interview', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Extracted text content
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    embedding_stored = db.Column(db.Boolean, default=False)

class JobDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    company = db.Column(db.String(255), nullable=True)
    source_type = db.Column(db.String(50), nullable=False)  # 'file', 'url', or 'text'
    source_data = db.Column(db.String(255), nullable=True)  # Filepath or URL
    content = db.Column(db.Text, nullable=False)  # Extracted or provided text content
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    embedding_stored = db.Column(db.Boolean, default=False)

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_description.id'))
    country = db.Column(db.String(100), nullable=True)
    accent = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    subtitles_enabled = db.Column(db.Boolean, default=True)
    
    resume = db.relationship('Resume')
    job_description = db.relationship('JobDescription')
    questions = db.relationship('InterviewQuestion', backref='interview', lazy=True)

class InterviewQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # 'icebreaker', 'technical', 'behavioral', etc.
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    answer = db.Column(db.Text, nullable=True)  # User's answer if stored

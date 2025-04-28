from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, Optional
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ResumeUploadForm(FlaskForm):
    resume = FileField('Upload Resume/CV', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'docx', 'txt'], 'Please upload a PDF, DOCX, or TXT file.')
    ])
    submit = SubmitField('Upload Resume')

class JobDescriptionForm(FlaskForm):
    source_type = RadioField('Job Description Source', choices=[
        ('file', 'Upload a file'),
        ('url', 'Provide a URL'),
        ('text', 'Enter text directly')
    ], default='file')
    
    job_file = FileField('Upload Job Description', validators=[
        FileAllowed(['pdf', 'docx', 'txt'], 'Please upload a PDF, DOCX, or TXT file.')
    ])
    
    job_url = StringField('Job Posting URL', validators=[
        Optional(), 
        URL(message='Please enter a valid URL.')
    ])
    
    job_text = TextAreaField('Enter Job Description')
    
    submit = SubmitField('Submit Job Description')

class InterviewSetupForm(FlaskForm):
    resume_id = SelectField('Select Resume', coerce=int)
    job_description_id = SelectField('Select Job Description', coerce=int)
    country = SelectField('Interview Country/Region', choices=[
        ('us', 'United States'),
        ('uk', 'United Kingdom'),
        ('australia', 'Australia'),
        ('india', 'India'),
        ('china', 'China'),
        ('canada', 'Canada'),
        ('singapore', 'Singapore'),
        ('germany', 'Germany')
    ])
    
    accent = SelectField('Interviewer Accent', choices=[
        ('us', 'US'),
        ('uk', 'UK'),
        ('australia', 'Australia'),
        ('india', 'India'),
        ('china', 'China')
    ])
    
    gender = SelectField('Interviewer Voice', choices=[
        ('male', 'Male'),
        ('female', 'Female')
    ])
    
    subtitles = BooleanField('Enable Subtitles', default=True)
    
    submit = SubmitField('Start Interview')

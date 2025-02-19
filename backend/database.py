from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_jwt_extended import JWTManager
from flask import Flask

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "your_secret_key"

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    files = db.relationship('AudioFile', backref='owner', lazy=True)

# Audio File Model
class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    processed_filename = db.Column(db.String(255), nullable=False)
    mfcc_image = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Create tables
with app.app_context():
    db.create_all()

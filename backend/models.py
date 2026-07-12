from datetime import datetime
from extensions import db
from flask_login import UserMixin
import enum
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole(enum.Enum):
    ADMIN = "Admin"
    TREK_STAFF = "Trek Staff"
    TREKKER = "Trekker"

class ProfileStatus(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class TrekStatus(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    OPEN = "Open"
    CLOSED = "Closed"
    COMPLETED = "Completed"

class BookingStatus(enum.Enum):
    BOOKED = "Booked"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class DifficultyLevel(enum.Enum):
    EASY = "Easy"
    MODERATE = "Moderate"
    HARD = "Hard"


class CommonFields(db.Model):
    """
    Abstract base class to provide common fields for all models.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(CommonFields, db.Model, UserMixin):
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.TREKKER)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    # Relationships
    bookings = db.relationship('Booking', backref='trekker', lazy=True)
    # Lazy relationship to find managed treks if the user is a Staff member
    managed_treks = db.relationship('Trek', backref='assigned_staff', lazy=True)
    staff_profile = db.relationship('StaffProfile', backref='user', uselist=False, lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Trekker(CommonFields):
    __tablename__ = 'trekkers'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    

class StaffProfile(CommonFields):
    __tablename__ = 'staff_profiles'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    contact_details = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum(ProfileStatus), default=ProfileStatus.PENDING)  # e.g., Active, On Leave
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    

class Trek(CommonFields):
    __tablename__ = 'treks'
    
    trek_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.Enum(DifficultyLevel), default=DifficultyLevel.EASY, nullable=False)  # Easy, Moderate, Hard
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(TrekStatus), default=TrekStatus.PENDING)  # Pending, Approved, Open, Closed, Completed
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    # Foreign Key linking to a User record whose role is 'Trek Staff'
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    bookings = db.relationship('Booking', backref='treks', lazy=True)


class Booking(CommonFields):
    __tablename__ = 'bookings'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.BOOKED)  # Booked, Cancelled, Completed
    

from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import celery
from celery_utils import make_celery
from extensions import mail, cache, db
from tasks import send_trek_reminder, send_say_hii
from flask_mail import Message
from config import Config
from celery.schedules import crontab
from models import User, UserRole, ProfileStatus, Trek
from routes import auth_bp, admin_bp, staff_bp, trekker_bp
from datetime import timedelta
from seed import seed_database


app = Flask(__name__)
CORS(app, resources = {"/api/*" : {"origins": "*"}}, supports_credentials=True)
# app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_SECRET_KEY'] = "23f3004091@ds.study.iitm.ac.in1234"
# app.config['beat_schedule'] = {
#     'daily-morning-reminders': {
#         'task': 'tasks.kickoff_daily_morning_reminders',
#         # 'schedule': 10.0,
#         'schedule': crontab(minute='*'), 
#     },
#     'monthly-trek-reports': {
#         'task': 'tasks.generate_monthly_trek_reports',
#         'schedule': crontab(minute='*'), 
#     }
# }
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "gyan02296@gmail.com" 
app.config['MAIL_PASSWORD'] = "lkltjyvrbuemadwe"
app.config['MAIL_DEFAULT_SENDER'] = "gyan02296@gmail.com"

app.config['broker_connection_retry_on_startup'] = True

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0' 
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['result_backend'] = 'redis://localhost:6379/2'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

mail.init_app(app)
db.init_app(app = app)
jwt = JWTManager(app)
celery = make_celery(app)
cache.init_app(app)


app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(staff_bp, url_prefix='/api/staff')
app.register_blueprint(trekker_bp, url_prefix='/api/trekker')

@app.route("/api/")
def index():
    return jsonify({"message": "Welcome to the Flask API!"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # seed_database()
        
    app.run(debug=True)

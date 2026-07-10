
from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import celery
from celery_utils import make_celery
from celery.schedules import crontab
# import tasks
from extensions import mail, cache, db
from tasks import send_trek_reminder, send_say_hii
from flask_mail import Message

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "23f3004091@ds.study.iitm.ac.in1234"
app.config['beat_schedule'] = {
    'daily-morning-reminders': {
        'task': 'tasks.kickoff_daily_morning_reminders',
        # 'schedule': 10.0, 
        'schedule': crontab(minute='*'), 
    },
    'monthly-trek-reports': {
        'task': 'tasks.generate_monthly_trek_reports',
        'schedule': crontab(minute='*'), 
    }
}
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "gyan02296@gmail.com" 
app.config['MAIL_PASSWORD'] = "lkltjyvrbuemadwe"
app.config['MAIL_DEFAULT_SENDER'] = "gyan02296@gmail.com"
app.config['broker_connection_retry_on_startup'] = True
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0' 
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['result_backend'] = 'redis://localhost:6379/2'

mail.init_app(app)
db.init_app(app = app)
jwt = JWTManager(app)
celery = make_celery(app)
cache.init_app(app)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Dummy check - replace with actual db query (e.g., User.query.filter_by...)
    if email == "admin@trek.com" and password == "123":
        # Create token with a role embedded (Admin, Trek Staff, or Trekker)
        access_token = create_access_token(identity=str({'email': email, 'role': 'Admin'}))
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad email or password"}), 401

@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    # Retrieves the identity we put in the token
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user, msg="Welcome to the protected dashboard!"), 200

@app.route('/api/treks', methods=['GET'])
@cache.cached(timeout=60) # Caches the response for 60 seconds
def get_treks():
    print("ROUTE EXECUTED: Cache was missed or expired!")
    treks = [
        {"id": 1, "name": "Himalaya Base Camp", "difficulty": "Hard"},
        {"id": 2, "name": "Sahyadri Ridge", "difficulty": "Medium"}
    ]
    return jsonify(treks), 200

@app.route('/api/send_reminder', methods=['POST'])
def send_reminder():
    # trek_id = request.json.get('trek_id')
    task = send_trek_reminder.delay(trek_id=1)  # Example trek_id
    return jsonify({"msg": "Reminder task has been queued.", "task_id": task.id}), 202

@app.route('/api/task_status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({"status": task.status, "result": task.result}), 200

@app.route('/api/trek_result/<task_id>', methods=['GET'])
def get_trek_result(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({"result": task.result}), 200


@app.route('/api/send_email', methods=['POST'])
def send_email():
    msg = Message("Hello from Trekking Management System",
                  recipients=["23f2001665@ds.study.iitm.ac.in"])
    mail.send(msg)
    return jsonify({"msg": "Email sent successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)


from celery.schedules import crontab

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "23f3004091@ds.study.iitm.ac.in1234"
    beat_schedule = {
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
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "gyan02296@gmail.com" 
    MAIL_PASSWORD = "lkltjyvrbuemadwe"
    MAIL_DEFAULT_SENDER = "gyan02296@gmail.com"
    broker_connection_retry_on_startup = True
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 300

    CACHE_REDIS_URL = 'redis://localhost:6379/0' 
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    result_backend = 'redis://localhost:6379/2'


from flask_mail import Mail
from flask_caching import Cache
from celery import Celery
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
celery = Celery()
mail = Mail()
cache = Cache()
import jwt
from flask import Flask, session, redirect, url_for, render_template, jsonify, request
import redis
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from functools import wraps
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from celery import Celery  # Add Celery import

db = SQLAlchemy()
migrate = Migrate()
from .models import Service, ServiceRequest, Professional, Customer

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

def create_app():
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SECRET_KEY'] = 'hhmanagement@1'
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household.db'
    app.secret_key = 'AJnHNHBSBSBGS565sf6fFrbXC32'
    app.config['JWT_ALGORITHM'] = 'HS256'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    
    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Allow CORS for all routes
    db.init_app(app)
    migrate.init_app(app,db)
    
    # Initialize caching
    cache = Cache(app)
    cache.init_app(app)

    # Initialize Redis client
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # Initialize Celery
    celery = make_celery(app)
    app.celery = celery  # Attach Celery instance to the app

    # Register Blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.customer import customer_bp
    from .routes.professional import professional_bp
    from .routes.v2 import v2_bp
    from .routes.email import email_bp  # Import the new email blueprint
    from .routes.report import report_bp  # Import the new report blueprint

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(professional_bp, url_prefix='/professional')
    app.register_blueprint(v2_bp, url_prefix='/api/v2')
    app.register_blueprint(email_bp, url_prefix='/email')  # Register the new email blueprint
    app.register_blueprint(report_bp, url_prefix='/report')  # Register the new report blueprint


    # Function to require JWT Token for protected routes
    def token_required(f):
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return jsonify({'error': 'Token is missing'}), 403
            try:
                print(token)
                jwt.decode(token, app.config['SECRET_KEY'], algorithms=app.config['JWT_ALGORITHM'])
            except Exception as error:
                return jsonify({'error': 'Token is invalid or expired'}), 403
            return f(*args, **kwargs)
        return decorated

    # Cache all GET requests dynamically
    @app.before_request
    def before_request():
        """Intercept GET requests and return cached responses if available."""
        if request.method == "GET":
            cache_key = request.full_path  # Unique cache key based on URL
            cached_response = cache.get(cache_key)
            if cached_response:
                return cached_response  # Return cached response if available

    # @app.after_request
    # def after_request(response):
    #     """Cache GET request responses dynamically."""
    #     if request.method == "GET":
    #         cache_key = request.full_path
    #         cache.set(cache_key, response.get_data(), timeout=1)  # Cache for 5 minutes
    #     return response

    # Routes
    @app.route("/access")
    @token_required
    def access():
        return jsonify({'message': 'Valid JWT token'})

    @app.route('/customer/logout')
    def logout():
        keys_to_remove = ['customer_id', 'customer_name']
        for key in keys_to_remove:
            session.pop(key, None)
        return redirect(url_for('auth.login'))

    @app.route('/admin/logout')
    def admin_logout():
        keys_to_remove = ['admin_id', 'admin_name']
        for key in keys_to_remove:
            session.pop(key, None)
        return redirect(url_for('auth.login'))

    @app.route('/professional/logout')
    def professional_logout():
        keys_to_remove = ['professional_id', 'professional_name']
        for key in keys_to_remove:
            session.pop(key, None)
        return redirect(url_for('auth.login'))

    @app.route('/')
    def index():
        return render_template('index.html', title='HH-Management')

    @app.route('/notautherized')
    def notautherized():
        return render_template('notautherized.html', title='HH-Management')

    # Route to check the status of the email sending task
    @app.route('/task_status/<task_id>', methods=['GET'])
    def task_status(task_id):
        task = celery.AsyncResult(task_id)
        if task is None or task.info is None:
            return jsonify({'status': 'unknown', 'message': 'Task not found or no information available'}), 404
        return jsonify({
            'status': task.info.get('status', 'unknown'),
            'result': task.info.get('result', None)
        })

    return app

from .tasks import send_bulk_email_task  # Import the Celery task

# Expose the Celery instance
celery = make_celery(create_app())
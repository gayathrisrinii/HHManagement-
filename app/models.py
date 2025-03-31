from . import db
from datetime import datetime

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    service_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    base_price = db.Column(db.Float, nullable=False)

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    service_request_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('professionals.pid'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), default="Requested")  # R = Requested, I = InProgress, C = Completed
    rating = db.Column(db.Integer, default=0)
    remarks = db.Column(db.Text, nullable=True)

class Professional(db.Model):
    __tablename__ = 'professionals'
    
    pid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=True)
    attachment = db.Column(db.String(200), nullable=True)  # Assuming this stores the file path
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    pin_code = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(10), default='Hold')  # Approve/Hold/Reject

class Customer(db.Model):
    __tablename__ = 'customers'
    
    customer_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    pin_code = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(20), nullable=True)



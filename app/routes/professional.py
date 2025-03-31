from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session
from app.forms import LoginForm, RegisterCusForm, RegisterProForm, ServiceForm, SearchForm
from app.models import Customer, Professional, Service, ServiceRequest
from app import db
from sqlalchemy import func

# Define the Blueprint for professional
professional_bp = Blueprint('professional', __name__)

# Route for Professional dashboard
@professional_bp.route('/dashboard')
def dashboard():
    if 'professional_id' not in session:
            flash('Please log in as professional to access the professionals dashboard.', 'warning')
            return redirect(url_for('auth.login'))
    Userdetails =Professional.query.filter_by(pid=session['professional_id']).first()
    servicehistory = ServiceRequest.query.filter_by(assignee_id=Userdetails.pid)
    serviceRequest = ServiceRequest.query.filter(ServiceRequest.status=='Requested')
    custinfo = Customer.query.filter()
    allservice=Service.query.filter()
    Custdetails = Customer.query.filter()
    return render_template('professional/dashboard.html',role="P", title="Professional Dashboard", ServiceRequests=serviceRequest,ServiceHistory=servicehistory,AllService=allservice, Custdetails=Custdetails,Custinfo=custinfo)
    
# Route for Professional Search
@professional_bp.route('/search')
def search():
    return render_template('professional/search.html',title='Professional Search',role="P")

# Route for Professional Insights
@professional_bp.route('/insights')
def insights():
    status_counts = db.session.query(
    ServiceRequest.status,
    func.count(ServiceRequest.status).label('count')).filter(ServiceRequest.assignee_id == session['professional_id']) \
    .group_by(ServiceRequest.status).all()

# Process results into the desired dictionary format
    chart_data = {
        "labels": [status for status, _ in status_counts],
        "values": [count for _, count in status_counts]
    }
    return render_template('professional/insights.html', title='Professional Insights',role="P", chart_data=chart_data)



@professional_bp.route('acceptser', methods=['GET'])
def acceptser():
    ID=request.args.get('id') 
    serviceRequest = ServiceRequest.query.get(ID)
    if serviceRequest is not None:
        serviceRequest.status = "InProgress"
        serviceRequest.assignee_id=session['professional_id']
        db.session.commit()
        flash('Service request accepted')
        return ({'success':True})
    else:
        flash('Service not found')
        return ({'success':False})



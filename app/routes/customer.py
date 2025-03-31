from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session
from app.forms import LoginForm, RegisterCusForm, RegisterProForm, ServiceForm, SearchForm
from app.models import Customer, Professional, Service, ServiceRequest
from app import db
from sqlalchemy import func


# Define the Blueprint for customer
customer_bp = Blueprint('customer', __name__)

# Route for the Customer dashboard
@customer_bp.route('/dashboard')
def dashboard():
    if 'customer_id' not in session:
            flash('Please log in as cusotmer to access the Customer dashboard.', 'warning')
            return redirect(url_for('auth.login'))
    Userdetails = Customer.query.filter_by(customer_id=session['customer_id']).first()
    Profdetails = Professional.query.filter()
    todayservices = Service.query.filter()
    servicehistory = ServiceRequest.query.filter_by(customer_id=Userdetails.customer_id)
    professionaldata= Professional.query.filter()
    
    return render_template('customer/dashboard.html', title="Customer Dashboard",role="C", TodayServices=todayservices, ServiceHistory=servicehistory,User=Userdetails,Professionaldata=professionaldata,Profdetails=Profdetails)


# Route for Customer Search
@customer_bp.route('/search')
def search():
    return render_template('customer/search.html',title='Customer Search',role="C")


# Route for Customer Insights
@customer_bp.route('/insights')
def insights():
    status_counts = db.session.query(
    ServiceRequest.status,
    func.count(ServiceRequest.status).label('count')).filter(ServiceRequest.customer_id == session['customer_id']) \
    .group_by(ServiceRequest.status).all()

# Process results into the desired dictionary format
    chart_data = {
        "labels": [status for status, _ in status_counts],
        "values": [count for _, count in status_counts]
    }

    return render_template('customer/insights.html',title='Customer Insights',role="C", chart_data=chart_data)

@customer_bp.route('/bookingdetails')
def bookingdetails():
    SID=request.args.get('sid') 
    if 'customer_id' not in session:
        flash('Please log in as cusotmer to access the Customer Service Request.', 'warning')
        return redirect(url_for('auth.login'))
    ServiceDetails = ServiceRequest.query.filter_by(service_request_id=SID).first()
    seviceinfo= Service.query.filter_by(id=ServiceDetails.service_id).first()
    professionalinfo= Professional.query.filter_by(pid=ServiceDetails.assignee_id).first()
    if ServiceDetails is not None and ServiceDetails.customer_id==session["customer_id"]:
        return render_template('customer/bookingdetails.html', title="Booking Details", role="C",ServiceDetails=ServiceDetails,SeviceInfo=seviceinfo,ProfessionalInfo=professionalinfo,sid=SID)
    else:
        return render_template('notautherized.html', title="not autherized")

@customer_bp.route('booknow', methods=['GET'])
def booknow():
    ID=request.args.get('packid') 
    if 'customer_id' not in session and session['type'] == 'C':
        flash('Please log in as cusotmer to access the Customer dashboard.', 'warning')
        return redirect(url_for('auth_bp.login'))
    Userdetails =Customer.query.filter_by(customer_id=session['customer_id']).first()
    if Userdetails is not None:
        newServiceRequest = ServiceRequest(
                customer_id=int(Userdetails.customer_id),
                service_id=ID,
            )
        db.session.add(newServiceRequest)
        db.session.commit()
        flash('Service Requested Successfully')
        return ({'success':True})
    else:
        flash('Service not found')
        return ({'success':False})
    


@customer_bp.route('cusservicelist',methods=["GET"])
def serviceslist():
    services = ServiceRequest.query.filter_by(customer_id=session['customer_id'])  # Retrieve all services
    results = {"data":[
        {
            "id": data.id,
            "service_name": data.service_name,
            "description": data.description,
            "category": data.category,  # Handle related data
            "base_price": data.base_price
        }
        for data in services
    ]}
    return jsonify(results)

@customer_bp.route('submit_rating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    sid=data.get('id')
    rateing=data.get('rating')
    remark=data.get('remark')
    serviceRequest = ServiceRequest.query.get(sid)
    if serviceRequest is not None:
        serviceRequest.rating = rateing
        serviceRequest.remarks=remark
        serviceRequest.status="Completed"
        db.session.commit()
        flash('Service request Rateing submitted Successfully')
        return ({'success':True})
    else:
        flash('Service not found')
        return ({'success':False})



    


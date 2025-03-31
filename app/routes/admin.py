from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session
from app.forms import LoginForm, RegisterCusForm, RegisterProForm, ServiceForm, SearchForm
from app.models import Customer, Professional, Service, ServiceRequest
from app import db
from sqlalchemy import func

# Define the Blueprint for admin
admin_bp = Blueprint('admin', __name__)

# Route for the Admin dashboard
@admin_bp.route('/dashboard',methods=["GET",'POST'])
def dashboard():
    if 'admin_id' not in session:
            flash('Please log in as admin to access the admins dashboard.', 'warning')
            return redirect(url_for('auth.login'))
    serviceform = ServiceForm()
    if serviceform.validate_on_submit():
        new_service = Service(
            service_name = serviceform.service_name.data,
            category = serviceform.category.data,
            description = serviceform.description.data,
            base_price = serviceform.base_price.data
        )
        try:
            # Assuming `new_customer` is an object you want to save with an ID attribute
            db.session.add(new_service)
            db.session.commit()
            flash("Service added")

        except Exception as e:
            # Roll back the session in case of an error
            db.session.rollback()
     
    
    profesionalpendings = Professional.query.filter(Professional.status == "Pending")
    return render_template('admin/dashboard.html', title="Admin Dashboard",role="A" ,ServiceForm=serviceform, ProfessionalStatus=profesionalpendings)

# Route for Admin Search
@admin_bp.route('/search')
def search():
    return render_template('admin/search.html',title="HH-Admin-Search",role="A" )

# Route for Admin Insights
@admin_bp.route('/insights')
def insights():
    status_counts = db.session.query(
    ServiceRequest.status,
    func.count(ServiceRequest.status).label('count')) \
    .group_by(ServiceRequest.status).all()
    cat_count = db.session.query(
    ServiceRequest.service_id,
    func.count(ServiceRequest.service_id).label('count')) \
    .group_by(ServiceRequest.service_id).all()
# Process results into the desired dictionary format
    chart_data = {
        "labels": [status for status, _ in status_counts],
        "values": [count for _, count in status_counts]
    }
    ServiceRequestCat_data = {
        "labels": [db.session.query(Service.service_name).filter(Service.id == service_id).first()[0] for service_id, _ in cat_count],
        "values": [count for _, count in cat_count]
    }
    return render_template('admin/insights.html', title='Admin Insights',role="A" , chart_data=chart_data, ServiceRequestCat_chart_data=ServiceRequestCat_data)



@admin_bp.route('acceptpro', methods=['GET'])
def acceptpro():
    ID=request.args.get('id') 
    user = Professional.query.get(ID)
    if user is not None:
        user.status = "Active"
        db.session.commit()
        flash('Professional '+user.full_name+' accepted')
        return ({'success':True})
    else:
        flash('Professional not found')
        return ({'success':False})

@admin_bp.route('rejectpro', methods=['GET'])
def rejectpro():
    ID=request.args.get('id') 
    user = Professional.query.get(ID)
    if user is not None:
        user.status = "Reject"
        db.session.commit()
        flash('Professional '+user.full_name+' rejected')
        return ({'success':True})
    else:
        flash('Professional not found')
        return ({'success':False})
    


@admin_bp.route('searchparameters',methods=["GET"])
def searchparameters():
    services = Service.query.all()  # Retrieve all services
    servicesRequests = ServiceRequest.query.all() # Retrieve all services
    professional = Professional.query.all() # Retrieve all Professionals List
    custombers = Customer.query.all() # Retrieve
    results = {"services":{"data":[
        {
            "id": data.id,
            "service_name": data.service_name,
            "description": data.description,
            "category": data.category,  # Handle related data
            "base_price": data.base_price
        }
        for data in services
    ]},
    "servicesRequests": {"data": [
        {
            "id": data.service_request_id,
            "customer_id": db.session.query(Customer.full_name).filter(Customer.customer_id == data.customer_id).first()[0], 
            "service_id":  db.session.query(Service.service_name).filter(Service.id == data.service_id).first()[0],
            "professsional_id":  db.session.query(Professional.full_name).filter(Professional.pid == data.assignee_id).first()[0] if db.session.query(Professional.full_name).filter(Professional.pid == data.assignee_id).first() else "Not Assigned",
            "status": data.status,
            "rating": data.rating

        }
        for data in servicesRequests
        ]},
        "professionals": {"data": [
            {
                "id": data.pid,
                "full_name": data.full_name,
                "email": data.email,
                "phone_number": data.phone,
                "status": data.status,
                "service_name":data.service_name
            }
            for data in professional
            ]},
            "customers": {"data": [
                {
                    "id": data.customer_id,
                    "full_name": data.full_name,
                    "email": data.email,
                    "phone_number": data.phone
                    }
                    for data in custombers
            ]}

    
    }

    return jsonify(results)


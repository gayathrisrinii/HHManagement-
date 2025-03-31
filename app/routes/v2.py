import jwt
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session,current_app
from app.models import Customer, Professional, Service, ServiceRequest
from app import db
import datetime



# Define the Blueprint for authentication
v2_bp = Blueprint('v2', __name__)

@v2_bp.route('/users',methods=['GET'])
def getUsers():
    users = Customer.query.all()
    users_list = [{ "email": user.email, "full_name": user.full_name, "phone": user.phone, "address": user.address, "pin_code": user.pin_code} for user in users]
    return jsonify({"isSuccess":True,"message":" submission successful","users":users_list}), 200

@v2_bp.route('/admin/get/services',methods=['GET'])
def getServices():
    services = Service.query.all()
    services_list = [
    {
        "service_name": service.service_name,
        "description": service.description,
        "category": service.category,
        "base_price": service.base_price,
        "id": service.id,

    } 
    for service in services]
    return jsonify({"isSuccess":True,"message":" submission successful","data":services_list}), 200

@v2_bp.route('/admin/get/servicerequests',methods=['GET'])
def getServiceRequests():
    data = ServiceRequest.query.all()
    customers = Customer.query.all()
    professionals = Professional.query.all()
    service= Service.query.all()
    sr_list = [
    {
        "date": sr.date,
        "customer_name": next((cus.full_name for cus in customers if cus.customer_id == sr.customer_id), None),
        "service_name": next((ser.service_name for ser in service if ser.id == sr.service_id), None),
        "assignee_id": next((prof.full_name for prof in professionals if prof.pid == sr.assignee_id), None),
        "status": sr.status,
        "rating": sr.rating,
        "id": sr.service_request_id
    } 
    for sr in data]
    return jsonify({"isSuccess":True,"message":" submission successful","data":sr_list}), 200


@v2_bp.route('/admin/get/professionals',methods=['GET'])
def getProfessionals():
    proff = Professional.query.all()
    prof_list = [
    {
        
        "pid": prof.pid,
        "full_name": prof.full_name,
        "email": prof.email,
        "phone": prof.phone,
        "status": prof.status,
        "experience": prof.experience,
    } 
    for prof in proff]
    return jsonify({"isSuccess":True,"message":" submission successful","data":prof_list}), 200

@v2_bp.route('/admin/get/customers',methods=['GET'])
def getCustomers():
    cust = Customer.query.all()
    cus_list = [
    {
        "full_name": cus.full_name,
        "email": cus.email,
        "phone": cus.phone,
        "id": cus.customer_id,
    } 
    for cus in cust]
    return jsonify({"isSuccess":True,"message":" submission successful","data":cus_list}), 200



@v2_bp.route('/admin/services',methods=['POST'])
def addServices():

    data=request.get_json()
    print(data.get('service_name'))
    new_service = Service(
        service_name = data.get('service_name'),
        category = data.get('category'),
        description = data.get('description'),
        base_price = data.get('base_price')
        )
    try:
        # Assuming `new_customer` is an object you want to save with an ID attribute
        db.session.add(new_service)
        db.session.commit()
        return jsonify({"isSuccess":True,"message":" Service added successfully"}), 200

    except Exception as e:
        # Roll back the session in case of an error
        db.session.rollback()
        return jsonify({"isSuccess":False,"message":"Failed to save service"}), 401




@v2_bp.route('/signup/customer',methods=['POST'])
def customerSignup():
    data=request.get_json()
    # Check if the email already exists
    existing_customer = Customer.query.filter_by(email=data.get('email')).first()
    if existing_customer:
        return jsonify({"isSuccess":False,"message":"Email already exists"}), 401

    new_user = Customer(
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        address=data.get('address'),
        pin_code=data.get('pin_code')
    )
    try:
        # Assuming `new_customer` is an object you want to save with an ID attribute
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"isSuccess":True,"message":"Customer "+data.get('full_name')+" submission successful"}), 200
       


    except Exception as e:
        # Roll back the session in case of an error
        db.session.rollback()
        print(e)
        return jsonify({"isSuccess":False,"message":"Failed to save customer"}), 401

        # Print the error message and the ID
        # print("An error occurred:", str(e))
        # print("Failed to save customer with ID:", getattr(new_user, 'id', 'No ID'))

        # Optionally, log more information or handle the error as needed

@v2_bp.route('/signup/professional',methods=['POST'])
def professionalSignup():
    data=request.get_json()
 
    new_user = Professional(
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        service_name=data.get('service_name'),
        experience=data.get('experience'),
        phone=data.get('phone'),
        address=data.get('address'),
        pin_code=data.get('pin_code')
    )
    try:
        # Assuming `new_professional` is an object you want to save with an ID attribute
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"isSuccess":True,"message":"professional "+data.get('full_name')+" submission successful"}), 200
       
    except Exception as e:
        # Roll back the session in case of an error
        db.session.rollback()
        return jsonify({"isSuccess":False,"message":"Failed to save professional"}), 401
    


# Route for login page
def generate_jwt_token(user, usertype, user_id, expiration_seconds=10000):
    """
    Generate a JWT token.
    :param user: Username or email of the user
    :param usertype: Type of the user (e.g., 'AL', 'PL', 'CL')
    :param user_id: ID of the user
    :param expiration_seconds: Token expiration time in seconds
    :return: Encoded JWT token
    """
    return jwt.encode(
        {
            'user': user,
            'usertype': usertype,
            'id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_seconds)
        },
        current_app.config['SECRET_KEY'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )

@v2_bp.route('/login', methods=['POST'])
def login():
        data=request.get_json()
        usertype = data.get('usertype')
        username = data.get('email')
        password = data.get('password')
        if(usertype and username and password):
            if usertype == 'AL':
                if username=="radmin@tm.od2.in" and password == "radmin@tm.od2.in":
                    session['admin_id'] = "1"
                    session['admin_name'] = "admin"
                    print(current_app.config['SECRET_KEY'])
                    

                    token = generate_jwt_token(username, usertype, "1")
                    return jsonify({"isSuccess":True,"token": token,"message":"Admin Login Success", "data":data}), 200
                else:
                    return jsonify({"isSuccess":False,"message":"Invalid User Credentials"}), 401

            elif usertype == 'PL':
                print(data)
                user = Professional.query.filter_by(email=username).first()
                print(user)
                if user and user.password == password and user.status == 'Active':
                    session['professional_id'] = user.pid
                    session['professional_name'] = user.full_name
                    token = generate_jwt_token(username, usertype, user.pid)
                    return jsonify({"isSuccess":True,"token": token,"message":"Login Success", "data":data}), 200
                elif user.status == 'Hold':
                    return jsonify({"message":"Your application is pending for approval by admin. Try again later"}), 401
                elif user.status == 'Reject':
                    return jsonify({"message":"Your application is rejected by admin. Try again later"}), 401
                else:
                    return jsonify({"isSuccess":False,"message":"Invalid User Credentials"}), 401
                    

            elif usertype == 'CL':
                user = Customer.query.filter_by(email=username).first()

                if user and user.password == password:
                    session['customer_id'] = user.customer_id
                    session['customer_name'] = user.full_name
                    token = generate_jwt_token(username, usertype, user.customer_id)
                    return jsonify({"isSuccess":True,"token": token,"message":"Login Success", "data":data}), 200
                    #return redirect(url_for('customer.dashboard'))
                else:
                    return jsonify({"isSuccess":False,"message":"Invalid User Credentials"}), 401
                    #flash("Invalid User Credentials")
                    #return render_template('auth/login.html', title="Login", LoginForm=loginform)
            else:
                flash("Invalid user type")
        else:
            return jsonify({"message":"Invalid Request"}), 401

@v2_bp.route('/admin/acceptpro', methods=['GET'])
def acceptProfessional():
    ID = request.args.get('id')
    user = Professional.query.get(ID)
    if user is not None:
        user.status = "Active"
        db.session.commit()
        return jsonify({'isSuccess': True, 'message': f'Professional {user.full_name} accepted'}), 200
    else:
        return jsonify({'isSuccess': False, 'message': 'Professional not found'}), 404

@v2_bp.route('/admin/rejectpro', methods=['GET'])
def rejectProfessional():
    ID = request.args.get('id')
    user = Professional.query.get(ID)
    if user is not None:
        user.status = "Reject"
        db.session.commit()
        return jsonify({'isSuccess': True, 'message': f'Professional {user.full_name} rejected'}), 200
    else:
        return jsonify({'isSuccess': False, 'message': 'Professional not found'}), 404

@v2_bp.route('/admin/deletepro', methods=['GET'])
def deleteProfessional():
    ID = request.args.get('id')
    user = Professional.query.get(ID)
    if user is not None:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'isSuccess': True, 'message': f'Professional {user.full_name} deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'isSuccess': False, 'message': 'Failed to delete professional'}), 500
    else:
        return jsonify({'isSuccess': False, 'message': 'Professional not found'}), 404

@v2_bp.route('/customer/get/servicerequest', methods=['GET'])
def getCustomerServiceRequest():
    ID = request.args.get('id')
    service_requests = ServiceRequest.query.filter_by(customer_id=ID).all()
    customers = Customer.query.all()
    professionals = Professional.query.all()
    services = Service.query.all()
    if service_requests:    
        service_requests_list = [
            {
                "service_request_id": sr.service_request_id,
                "service_id": sr.service_id,
                "customer_id": sr.customer_id,
                "date": sr.date,
                "status": sr.status,
                "rating": sr.rating,
                "customer_name": next((cus.full_name for cus in customers if cus.customer_id == sr.customer_id), None),
                "service_name": next((svc.service_name for svc in services if svc.id == sr.service_id), None),
                "description": next((svc.description for svc in services if svc.id == sr.service_id), None),
                "professional_name": next((prof.full_name for prof in professionals if prof.pid == sr.assignee_id), None),
            }
            for sr in service_requests
        ]
        return jsonify({'isSuccess': True, 'data': service_requests_list}), 200
    else:
        return jsonify({'isSuccess': False, 'message': 'Service requests not found'}), 404
    
@v2_bp.route('/professional/get/servicerequest1', methods=['GET'])
def get_requested_service_requests():
    status = request.args.get('status')  # Get 'status' query parameter
    
    # Query for service requests with the specified status
    service_requests_query = ServiceRequest.query.filter_by(status=status)  # Apply filter first
    service_requests = service_requests_query.all()
    # Get all customers and services
    customers = Customer.query.all()
    services = Service.query.all()

    if service_requests:
        service_requests_list = [
            {
                "service_request_id": sr.service_request_id,
                "date": sr.date,
                "status": sr.status,
                "customer_name": next((cus.full_name for cus in customers if cus.customer_id == sr.customer_id), None),
                "service_name": next((svc.service_name for svc in services if svc.id == sr.service_id), None)
            }
            for sr in service_requests
        ]
        return jsonify({'isSuccess': True, 'data': service_requests_list}), 200
    else:
        return jsonify({'isSuccess': False, 'message': 'Service requests not found'}), 404


@v2_bp.route('/professional/get/servicerequest2', methods=['GET'])
def get_service_requests_by_professional():
    professional_id = request.args.get('id')  # Get 'id' query parameter

    # Query for service requests assigned to the specified professional
    service_requests_query = ServiceRequest.query.filter_by(assignee_id=professional_id)
    service_requests = service_requests_query.all()
    # Get all customers and services
    customers = Customer.query.all()
    services = Service.query.all()

    if service_requests:
        service_requests_list = [
            {
                "service_request_id": sr.service_request_id,
                "date": sr.date,
                "status": sr.status,
                "customer_name": next((cus.full_name for cus in customers if cus.customer_id == sr.customer_id), None),
                "service_name": next((svc.service_name for svc in services if svc.id == sr.service_id), None)
            }
            for sr in service_requests
        ]
        return jsonify({'isSuccess': True, 'data': service_requests_list}), 200
    else:
        return jsonify({'isSuccess': False, 'message': 'Service requests not found'}), 404

@v2_bp.route('/customer/booknow', methods=['POST'])
def booknow():
    data = request.get_json()
    service_id = data.get('service_id')
    customer_id = data.get('customer_id')
    if not customer_id:
        return jsonify({'isSuccess': False, 'message': 'Please log in as a customer to book a service'}), 401

    user_details = Customer.query.filter_by(customer_id=customer_id).first()
    service_details = Service.query.filter_by(id=service_id).first()

    if not service_details:
        return jsonify({'isSuccess': False, 'message': 'Service not found'}), 404

    if user_details:
        new_service_request = ServiceRequest(
            customer_id=customer_id,
            service_id=service_id,
        )
        try:
            db.session.add(new_service_request)
            db.session.commit()
            return jsonify({'isSuccess': True, 'message': 'Service requested successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'isSuccess': False, 'message': 'Failed to request service'}), 500
    else:
        return jsonify({'isSuccess': False, 'message': 'Customer not found'}), 404
    
@v2_bp.route('/customer/completenow', methods=['POST'])
def completenow():
    data = request.json
    service_request_id = data.get('service_request_id')
    rating = data.get('rating')
    remarks = data.get('remarks')
    
    service_request = ServiceRequest.query.get(service_request_id)
    if service_request and service_request.status != "Completed":
        service_request.status = "Completed"
        service_request.rating = rating
        service_request.remarks = remarks
        db.session.commit()
        return jsonify({'isSuccess': True, 'message': 'Service completed successfully'}), 200
    else:
        return jsonify({'isSuccess': False, 'message': 'Invalid service or already completed'}), 400

@v2_bp.route('/professional/accept-service', methods=['POST'])
def accept_service():
    data = request.get_json()
    service_request_id = data.get('service_request_id')
    professional_id = data.get('professional_id')
    print(data,service_request_id,professional_id)

    if not professional_id:
        return jsonify({'isSuccess': False, 'message': 'Please log in as a professional to accept a service'}), 401

    service_request = ServiceRequest.query.get(service_request_id)
    if service_request is not None:
        service_request.status = "InProgress"
        service_request.assignee_id = professional_id
        try:
            db.session.commit()
            return jsonify({'isSuccess': True, 'message': 'Service request accepted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'isSuccess': False, 'message': 'Failed to accept service request'}), 500
    else:
        return jsonify({'isSuccess': False, 'message': 'Service request not found'}), 404
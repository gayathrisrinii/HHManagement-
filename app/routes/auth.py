from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session
from app.forms import LoginForm, RegisterCusForm, RegisterProForm, ServiceForm, SearchForm
from app.models import Customer, Professional, Service, ServiceRequest
from app import db

# Define the Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Route for login page
@auth_bp.route('/login', methods=["GET",'POST'])
def login():

    loginform = LoginForm()
    
    if loginform.validate_on_submit():
        usertype=loginform.usertype.data
        username=loginform.username.data
        password=loginform.password.data
        if(usertype and username and password):
            if usertype == 'AL':
                if username=="admin" and password == "admin":
                    session['admin_id'] = "1"
                    session['admin_name'] = "admin"
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash("Invalid User Credentials")
                    return render_template('auth/login.html', title="Login", LoginForm=loginform)

            elif usertype == 'PL':
                user = Professional.query.filter_by(email=username).first()
                if user and user.password == password and user.status == 'Active':
                    session['professional_id'] = user.pid
                    session['professional_name'] = user.full_name
                    flash("Login Success")
                    return redirect(url_for('professional.dashboard'))
                elif user.status == 'Pending':
                    flash("Your application is pending")
                elif user.status == 'Reject':
                    flash("Your application is rejected by admin. Try again later")
                else:
                    flash("Invalid User Credentials")
                    return render_template('auth/login.html', title="Login", LoginForm=loginform)

            elif usertype == 'CL':
                user = Customer.query.filter_by(email=username).first()

                if user and user.password == password:
                    session['customer_id'] = user.customer_id
                    session['customer_name'] = user.full_name
                    flash(f'Welcome, {user.full_name}!', 'success')
                    return redirect(url_for('customer.dashboard'))
                else:
                    flash("Invalid User Credentials")
                    return render_template('auth/login.html', title="Login", LoginForm=loginform)
            else:
                flash("Invalid user type")
        else:
            flash("Please fill in all fields")
    return render_template('auth/login.html', title="Login", LoginForm=loginform)



@auth_bp.route('signup/customer',methods=["GET",'POST'])
def customerSignup():
    registerform=RegisterCusForm()
    if registerform.validate_on_submit():
        new_user = Customer(
            email=registerform.email.data,
            password=registerform.password.data,
            full_name=registerform.full_name.data,
            phone=registerform.phone.data,
            address=registerform.address.data,
            pin_code=registerform.pin_code.data
        )
        try:
            # Assuming `new_customer` is an object you want to save with an ID attribute
            db.session.add(new_user)
            db.session.commit()
            flash("Customer "+registerform.full_name.data+" submission successful")


        except Exception as e:
            # Roll back the session in case of an error
            db.session.rollback()
            # Print the error message and the ID
            # print("An error occurred:", str(e))
            # print("Failed to save customer with ID:", getattr(new_user, 'id', 'No ID'))

            # Optionally, log more information or handle the error as needed


    return render_template('auth/customersignup.html', title="Customer Signup", RegisterForm=registerform)

@auth_bp.route('signup/professional',methods=["GET",'POST'])
def professionalSignup():
    registerform=RegisterProForm()
    if request.method == 'POST':
        if registerform.validate_on_submit():
            new_user = Professional(
                email=registerform.email.data,
                password=registerform.password.data,
                full_name=registerform.full_name.data,
                phone=registerform.phone.data,
                address=registerform.address.data,
                pin_code=registerform.pin_code.data,
                service_name=registerform.service_name.data,
                experience=registerform.experience.data,
                status=registerform.status.data,
            )
            try:
                flash('Registration successful')

                # Assuming `new_customer` is an object you want to save with an ID attribute
                db.session.add(new_user)
                db.session.commit()
                # print("Form submission successful", new_user.id)

            except Exception as e:
                # Roll back the session in case of an error
                db.session.rollback()
                # Print the error message and the ID
                # print("An error occurred:", str(e))
                # print("Failed to save customer with ID:", getattr(new_user, 'id', 'No ID'))
        else:
            # Debugging failed validations
            for field, errors in registerform.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
            return "Form validation failed. Check the logs for details."

    return render_template('auth/professionalsignup.html', title="Professional Signup", RegisterForm=registerform)


@auth_bp.route('serviceslist',methods=["GET"])
def serviceslist():
    services = Service.query.all()  # Retrieve all services
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
    

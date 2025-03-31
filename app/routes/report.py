from flask import Blueprint, request, jsonify, current_app, render_template
from ..tasks import send_bulk_email_task, send_inprogress_email_task, generate_csv_report_task  # Update the import statement
from ..models import Professional, ServiceRequest, Service
from ..email_utils import send_email, send_inprogress_task_email  # Update the import statement
from datetime import datetime, timedelta

report_bp = Blueprint('report', __name__)

# New route to generate PDF report and send to admin
@report_bp.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.get_json()
    admin_email = data.get('admin_email')
    report_type = data.get('report_type', 'daily')  # Get report type from the request, default to 'daily'

    if not admin_email:
        return jsonify({'error': 'Admin email is required'}), 400

    # Fetch report data from the database
    report_data = []
    professionals = Professional.query.all()
    for professional in professionals:
        service_requests = ServiceRequest.query.filter_by(assignee_id=professional.pid).all()
        for service_request in service_requests:
            service = Service.query.get(service_request.service_id)
            report_data.append([
                professional.full_name,
                service_request.status,
                service.service_name
            ])

    # Calculate the total number of requests and their statuses based on report type
    if report_type == 'daily':
        start_date = datetime.utcnow().date()
    elif report_type == 'monthly':
        start_date = (datetime.utcnow() - timedelta(days=30)).date()
    else:
        return jsonify({'error': 'Invalid report type'}), 400

    total_requests = ServiceRequest.query.filter(ServiceRequest.date >= start_date).count()
    resolved_requests = ServiceRequest.query.filter(ServiceRequest.date >= start_date, ServiceRequest.status == 'Completed').count()
    pending_requests = ServiceRequest.query.filter(ServiceRequest.date >= start_date, ServiceRequest.status == 'InProgress').count()
    requested_requests = ServiceRequest.query.filter(ServiceRequest.date >= start_date, ServiceRequest.status == 'Requested').count()

    summary_data = [
        ['total_requests', total_requests],
        ['resolved_requests', resolved_requests],
        ['pending_requests', pending_requests],
        ['requested_requests', requested_requests]
    ]

    # Call the Celery task to generate CSV and send email
    task = generate_csv_report_task.delay(admin_email, report_data, summary_data, report_type)
    return jsonify({'task_id': task.id}), 202

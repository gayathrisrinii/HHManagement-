from flask import Blueprint, request, jsonify, current_app, render_template
from ..tasks import send_bulk_email_task, send_inprogress_email_task
from ..models import Professional, ServiceRequest, Service
from ..email_utils import send_email, send_inprogress_task_email  # Update the import statement

email_bp = Blueprint('email', __name__)

@email_bp.route('/send_bulk_email', methods=['POST'])
def send_bulk_email():
    data = request.get_json()
    subject = data.get('subject')
    message = data.get('message')
    recipients = data.get('recipients', [])

    if not subject or not message or not recipients:
        return jsonify({'error': 'Subject, message, and recipients are required'}), 400

    # Call the Celery task
    task = send_bulk_email_task.delay(subject, message, recipients)
    return jsonify({'task_id': task.id}), 202


@email_bp.route('/trigger_inprogress_email', methods=['POST'])
def trigger_inprogress_email():
    task = send_inprogress_email_task.delay()
    return jsonify({'task_id': task.id}), 202

from flask import render_template
from .models import Professional, ServiceRequest, Service
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(subject, message_html, recipients, attachments=None):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    sent_count = 0
    not_sent_count = 0
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for recipient in recipients:
            try:
                msg = MIMEMultipart('alternative')  # Use 'alternative' to support HTML
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                message_plain = "Your tasks are in progress. Please check your email client for the HTML version."
                msg.attach(MIMEText(message_plain, 'plain'))
                msg.attach(MIMEText(message_html, 'html', 'utf-8'))  # Attach the message as HTML with UTF-8 encoding

                # Attach files if any
                if attachments:
                    print(attachments)
                    for attachment in attachments:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment['content'])
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename={attachment["filename"]}')
                        msg.attach(part)

                server.sendmail(sender_email, recipient, msg.as_string())
                sent_count += 1
            except Exception:
                not_sent_count += 1

        server.quit()
        return {'message': 'Emails sent successfully', 'sent_count': sent_count, 'not_sent_count': not_sent_count}
    except Exception as e:
        return {'error': str(e), 'sent_count': sent_count, 'not_sent_count': not_sent_count}

def send_inprogress_task_email():
    professionals = Professional.query.join(ServiceRequest, Professional.pid == ServiceRequest.assignee_id)\
                                      .filter(ServiceRequest.status == 'InProgress').all()
    total_sent_count = 0
    total_not_sent_count = 0
    
    for professional in professionals:
        service_requests = ServiceRequest.query.filter_by(assignee_id=professional.pid, status='InProgress')\
                                               .join(Service, ServiceRequest.service_id == Service.id)\
                                               .add_columns(Service.service_name, Service.description, ServiceRequest.date, ServiceRequest.remarks).all()
        if service_requests:
            subject = "Tasks In Progress"
            service_requests_data = [{'service_name': sr.service_name, 'description': sr.description, 'date': sr.date, 'remarks': sr.remarks} for sr in service_requests]
            message_html = render_template('inprogress_task_email.html', professional=professional, service_requests=service_requests_data)
            result = send_email(subject, message_html, [professional.email])
            total_sent_count += result['sent_count']
            total_not_sent_count += result['not_sent_count']
    
    return {'message': 'Emails sent successfully', 'sent_count': total_sent_count, 'not_sent_count': total_not_sent_count}

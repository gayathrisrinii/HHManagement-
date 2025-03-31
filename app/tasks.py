from celery import Celery
from celery.schedules import crontab  # Import crontab for scheduling
from .email_utils import send_inprogress_task_email, send_email
from . import create_app  # Import the create_app function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from flask import current_app, render_template  # Import render_template
import csv  # Import csv module
from datetime import datetime  # Import datetime module

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Configure Celery beat schedule
celery.conf.beat_schedule = {
    'send-inprogress-email-every-day-at-6pm': {
        'task': 'app.tasks.send_inprogress_email_task',
        'schedule': crontab(hour=18, minute=0),  # Schedule to run at 6 PM every day
        # 'schedule': crontab(day_of_week='monday', hour=18, minute=0),  # Schedule to run every Monday at 6 PM
        # 'schedule': crontab(minute='*/1'),  # Schedule to run every minute for testing
    },
}

celery.conf.timezone = 'UTC'  # Ensure timezone is set

@celery.task(bind=True)
def send_bulk_email_task(self, subject, message, recipients, attachments=None):
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
                msg.attach(MIMEText(message, 'html', 'utf-8'))  # Attach the message as HTML with UTF-8 encoding

                # Attach files if any
                if attachments:
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
        self.update_state(state='FAILURE', meta={'error': str(e), 'sent_count': sent_count, 'not_sent_count': not_sent_count})
        return {'error': str(e), 'sent_count': sent_count, 'not_sent_count': not_sent_count}

@celery.task
def send_inprogress_email_task():
    print("Scheduler triggered: send_inprogress_email_task is running")  # Print statement to indicate task run
    app = create_app()  # Create the Flask app
    with app.app_context():
        result = send_inprogress_task_email()
    return result

@celery.task(bind=True)
def generate_csv_report_task(self, admin_email, report_data, summary_data, report_type):
    app = create_app()  # Create the Flask app
    with app.app_context():
        try:
            self.update_state(state='PROGRESS', meta={'status': 'Generating CSV report'})
            
            # Generate a unique filename for the report
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            csv_filename = f'{report_type}_report_{timestamp}.csv'

            # Generate CSV report
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Add a heading to the report
                writer.writerow([f'{report_type.capitalize()} Report'])
                writer.writerow([])  # Blank line for separation
                
                # Add report data
                writer.writerow(['Report Data'])
                writer.writerow(['Professional', 'Service Request Status', 'Service'])
                writer.writerows(report_data)
                writer.writerow([])  # Blank line for separation
                
                # Add summary data
                writer.writerow(['Summary Data'])
                writer.writerows(summary_data)

            with open(csv_filename, 'rb') as csvfile:
                csv_data = csvfile.read()

            self.update_state(state='PROGRESS', meta={'status': 'CSV report generated successfully'})
        except Exception as e:
            self.update_state(state='FAILURE', meta={'error': str(e)})
            return {'error': str(e)}

        # Determine the subject based on report type
        subject = f'Admin {report_type.capitalize()} Report'

        # Prepare attachments
        attachments = [{'filename': csv_filename, 'content': csv_data}] if csv_data else []
        print(f"Attachments: {attachments}")

        try:
            self.update_state(state='PROGRESS', meta={'status': 'Sending email with CSV attachment'})
            # Send email with CSV attachment
            send_email(
                subject=subject,
                message_html='Please find the attached report.',
                recipients=[admin_email],
                attachments=attachments
            )
            self.update_state(state='SUCCESS', meta={'status': 'Email sent successfully'})
            return {'status': 'Email sent successfully'}
        except Exception as e:
            self.update_state(state='FAILURE', meta={'error': str(e)})
            return {'error': str(e)}

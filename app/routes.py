from flask import Flask, render_template, request, redirect, url_for
import psutil  # Import the 'psutil' library for system monitoring
import ezgmail  # Import the 'ezgmail' library for sending emails
from config import EMAIL_ADDRESS

from app import app

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/check_metrics', methods=['POST'])
def check_metrics():
    print('hello')
    # cpu_usage = psutil.cpu_percent(interval=None)

    cpu_usage = 1
    # if cpu_usage > 1:  # Set your desired CPU threshold here
    subject = "High CPU Usage Alert"
    body = f"CPU usage is {cpu_usage}% which is above the threshold."
        
    try:
        ezgmail.send(EMAIL_ADDRESS, subject, body)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", str(e))
            
    return "Metrics checked and email sent if necessary."

from flask import Flask, render_template, request, redirect, url_for
import psutil  # Import the 'psutil' library for system monitoring
import ezgmail  # Import the 'ezgmail' library for sending emails
from config import EMAIL_ADDRESS
import time

from app import app

@app.route('/')
def index():
      # Add code here to retrieve server performance data using psutil
    # Store the data in suitable variables to pass to the template
    # Example data for demonstration purposes
    
    start_time = time.time()  # Record the start time
    cpu_usage = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    total_memory = memory.total
    available_memory = memory.available
    memory_usage = memory.percent
    disk_usage = psutil.disk_usage('/')
    total_disk_space = disk_usage.total
    used_disk_space = disk_usage.used
    free_disk_space = disk_usage.free
    disk_space_usage = disk_usage.percent
    network_stats = psutil.net_io_counters()
    bytes_sent = network_stats.bytes_sent
    bytes_received = network_stats.bytes_recv
    packets_sent = network_stats.packets_sent
    packets_received = network_stats.packets_recv
    end_time = time.time()  # Record the end time
    response_time = end_time - start_time  # Calculate response time in seconds

  

    return render_template('index.html',
                           cpu_usage=cpu_usage,
                           total_memory=total_memory, available_memory=available_memory,
                           memory_usage=memory_usage, total_disk_space=total_disk_space,
                           used_disk_space=used_disk_space, free_disk_space=free_disk_space,
                           disk_space_usage=disk_space_usage, bytes_sent=bytes_sent,
                           bytes_received=bytes_received, packets_sent=packets_sent,
                           packets_received=packets_received, response_time=response_time)


@app.route('/check_metrics', methods=['POST'])
def check_metrics():
    print('hello')
    cpu_usage = psutil.cpu_percent(interval=None)

    # cpu_usage = 1
    if cpu_usage > 1:  # Set your desired CPU threshold here
        subject = "High CPU Usage Alert"
        body = f"CPU usage is {cpu_usage}% which is above the threshold."
        
    try:
        ezgmail.send(EMAIL_ADDRESS, subject, body)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", str(e))
            
    return "Metrics checked and email sent if necessary."

if __name__ == '__main__':
    app.run()

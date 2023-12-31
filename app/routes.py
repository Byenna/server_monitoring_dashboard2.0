from flask import render_template, request
import psutil  # Import the 'psutil' library for system monitoring
import ezgmail  # Import the 'ezgmail' library for sending emails
import config 
import time
from app import app
import secrets


SECRET_KEY = secrets.token_hex(32)

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
    csrf_token = config.csrf_token
    email_address = config.EMAIL_ADDRESS 
    print('hello SRE')
    cpu_usage = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    network_stats = psutil.net_io_counters()
    start_time = time.time()  # Record the start time
    end_time = time.time()  # Record the end time
    response_time = end_time - start_time  # Calculate response time in seconds

    alerts = []  # Create a list to store alert messages

    if cpu_usage > 100:  # Set your desired CPU threshold here
        cpu_alert = f"CPU usage is {cpu_usage}% which is above the threshold."
        alerts.append(("High CPU Usage Alert", cpu_alert))
    
    if memory.percent > 100:  # Set your desired Memory threshold here
        memory_alert = f"Memory usage is {memory.percent}% which is above the threshold."
        alerts.append(("High Memory Usage Alert", memory_alert))
    
    if disk_usage.percent > 100:  # Set your desired Disk threshold here
        disk_alert = f"Disk usage is {disk_usage.percent}% which is above the threshold."
        alerts.append(("High Disk Usage Alert", disk_alert))
    
    if network_stats.bytes_sent > 10000000:  # Set your desired Network threshold here
        network_alert = f"Network sent bytes exceed the threshold."
        alerts.append(("High Network Usage Alert", network_alert))
    
    if response_time > 100:  # Set your desired Response Time threshold here
        response_alert = f"Response time is {response_time} seconds which is above the threshold."
        alerts.append(("Slow Response Alert", response_alert))

    # Send alert emails for each condition
    for subject, body in alerts:
        try:
            ezgmail.send(config.EMAIL_ADDRESS, subject, body)
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email:", str(e))
    
        
    
            
    return render_template('check_metrics.html', csrf_token=csrf_token, config=config)

    
    


if __name__ == '__main__':
    app.run()

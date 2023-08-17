from flask import Flask
import ezgmail  # Import the 'ezgmail' library

# Create the Flask app instance
app = Flask(__name__)

try:
    ezgmail.init()
    print("SMTP login successful.")
except ezgmail.SMTPAuthenticationError:
    print("SMTP login failed. Check if Less secure app access is enabled.")
except Exception as e:
    print("An error occurred:", str(e))

# Import routes to ensure they are registered with the app
from app import routes

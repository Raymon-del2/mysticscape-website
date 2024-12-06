import sys
import os

# Add your project directory to the sys.path
project_home = '/home/your_pythonanywhere_username/mysticscape/website'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your Flask app
from app import app as application

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['DATABASE_URL'] = 'mysql://username:password@hostname/database_name'

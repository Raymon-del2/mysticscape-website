import sys
import os

# Add your project directory to the sys.path
project_home = '/home/LucidRealms/mysticscape/website'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your app
from app import app as application

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Root entry point for Azure App Service & Cloud hosting providers
from dashboard.app import *

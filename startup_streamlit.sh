#!/bin/bash
# Azure App Service startup script for Streamlit Dashboard
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run dashboard/app.py --server.port 8000 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false

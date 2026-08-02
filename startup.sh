#!/bin/bash
# Azure App Service Linux startup script
PORT_TO_USE="${PORT:-8080}"
echo "Starting Streamlit on port $PORT_TO_USE..."

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run dashboard/app.py --server.port $PORT_TO_USE --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false

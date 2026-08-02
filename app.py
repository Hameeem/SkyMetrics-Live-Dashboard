import sys, os, subprocess

if __name__ == "__main__":
    port = os.getenv("PORT", "8080")
    cmd = [
        sys.executable, "-m", "streamlit", "run", "dashboard/app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    print(f"Launching Streamlit on Azure port {port}...")
    subprocess.run(cmd)
else:
    # Import dashboard module
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    from dashboard.app import *

import sys
import os

# Ensure the backend folder is in the python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

if __name__ == "__main__":
    # We use 0.0.0.0 to ensure it listens on all local interfaces
    # This is also what you will need for AWS EC2 later!
    app.run(host='0.0.0.0', port=5000, debug=True)
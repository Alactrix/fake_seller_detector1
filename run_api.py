# run_api.py (place in root folder)
from api.server import app

if __name__ == '__main__':
    app.run(port=5000, debug=True)
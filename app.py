from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return {
        "message": "Hello from DevOps Project!",
        "version": "1.0",
        "host": os.environ.get("HOSTNAME", "unknown")
    }

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

@app.route('/metrics')
def metrics():
    return "# App is running\napp_up 1\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

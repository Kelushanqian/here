# app.py
# 程序入口

import os
import threading
from flask import Flask
from config import ORIGINAL_DIR, PROCESSED_DIR
from worker import worker_loop
from routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    os.makedirs(ORIGINAL_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()

    app.run(host='0.0.0.0', port=5001, debug=True)
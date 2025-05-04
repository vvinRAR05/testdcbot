import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

def run():
    port = int(os.getenv("PORT", 8080))  # Render setzt PORT automatisch
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

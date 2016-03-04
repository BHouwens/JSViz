from flask import Flask, render_template
from services.controller import Controller
from services.npm import NPMHunter

import os


app = Flask(__name__)

@app.route('/')
def home():
    root = NPMHunter(os.getcwd())
    start = root.find_start()
    print start
    return render_template('index.html', start = '')
        
if __name__ == '__main__':
    app.run(debug=True)
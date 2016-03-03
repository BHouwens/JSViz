from flask import Flask, render_template
from services.npm import NPMHunter
from services.grunt import GruntHunter

import os


app = Flask(__name__)

@app.route('/')
def home():
    npm = NPMHunter(os.getcwd())
    start = npm.find_start()
    
    return render_template('index.html', start = start)
        
if __name__ == '__main__':
    app.run(debug=True)
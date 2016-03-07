from flask import Flask, render_template
from services.languages.typescript import TypeScriptHunter
from services.task_runners.npm import NPMHunter
from services.task_runners.webpack import WebpackHandler
from services.controller import Controller

import os


app = Flask(__name__)

@app.route('/')
def home():
    t = WebpackHandler('/Users/byronhouwens/ABGlobal/ksys336')
    
    return render_template('index.html', task_runners = '')
        
if __name__ == '__main__':
    app.run(debug=True)
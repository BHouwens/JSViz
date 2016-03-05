from flask import Flask, render_template
from services.languages.typescript import TypeScriptHunter

import os


app = Flask(__name__)

@app.route('/')
def home():
    t = TypeScriptHunter('/Users/byronhouwens/ABGlobal/ksys336')
    t.crawl_tsd()
    print t.extensions
    return render_template('index.html', task_runners = '')
        
if __name__ == '__main__':
    app.run(debug=True)
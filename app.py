import os

from flask import Flask, jsonify
from services.controller import Controller

app = Flask(__name__)
path = '/Users/byronhouwens/ABGlobal/ksys336'
ctrl = Controller(path)

@app.route('/')
def home():
    stats = {
        'path' : path
    }
    
    return jsonify(stats)
 
@app.route('/task-runners')
def task_runners():
    return jsonify({'task_runners': ctrl.task_runners})
      
if __name__ == '__main__':
    app.run(debug=True)
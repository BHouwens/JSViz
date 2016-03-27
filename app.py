from flask import Flask, jsonify, render_template
from services.controller import Controller
from services.networker import Networker

app = Flask(__name__)
path = '/Users/byronhouwens/ksys326'
ctrl = Controller(path)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/handlers')
def handlers():
    return jsonify({'handlers': ctrl.handlers})
 
@app.route('/task-runners')
def task_runners():
    return jsonify({'task_runners': ctrl.task_runners})
    
@app.route('/network')
def network():
    n = Networker(path, ['*.ts', '*.js'])
    n.find_dependents()
    
    return jsonify({'files': n.files, 'links': n.links})
    
@app.route('/d3')
def d3():
    return jsonify({'nodes': ctrl.nodes, 'links': ctrl.links})
      
if __name__ == '__main__':
    app.run(debug=True)
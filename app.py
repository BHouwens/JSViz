from flask import Flask, jsonify, render_template
from services.networker import Networker, import_handler

app = Flask(__name__)
path = '/Users/byronhouwens/pyramid'

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/network')
def network():
    n = Networker(path, ['*.py', '*.html'])
    n.find_dependents()
    
    print 'length of nodes: {0}'.format(len(n.files))
    
    return jsonify({'files': n.files, 'links': n.links})
      
if __name__ == '__main__':
    app.run(debug=True)
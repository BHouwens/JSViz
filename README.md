# PyViz

Just a tool to visualise Python project structures. Really useful for larger projects

## Install

    virtualenv venv
    source venv/bin/activate
    npm i --save
    npm start
    
This will build Webpack and start the Flask app on port 5000

## Todo

- Add support for imports from a folder higher up the project tree
- Add metadata to nodes to surface on UI (work external deps into this)
- (?) Set up special styles for files like `setup.py` and requirements

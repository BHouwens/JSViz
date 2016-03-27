# JSViz

Just a tool to visualise JavaScript (and all its various flavours) project structures. 

The idea is to visualise the relationships between files, creating a network via their dependencies
and dependents, as well as the task runners and such that kick a project off.

## Install

    virtualenv venv
    source venv/bin/activate
    npm i --save
    npm start
    
This will build Webpack and start the Flask app on port 5000

## Todo

Too much:

- Add support for more unusual import methods
- Tie generic file networks to their task runners/`package.jsons`
- Add support and detection for other flavours/languages of JS
- Add support for virtually all task runners 

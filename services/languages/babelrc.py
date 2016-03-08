import os, json

def babelrc_exists(path):
    """
    Returns whether Babel is active via .babelrc
    in the supplied path or not
    """
    os.chdir(path)
    active = False
    
    if os.path.isfile('.babelrc'):
        active = True
    
    return active
    
def babel_plugins(path):
    """
    Returns list of Babel plugins used in the project
    """
    os.chdir(path)
    
    if os.path.isfile('.babelrc'):
        with open('.babelrc', 'r') as file:
            j_data = file.read().decode('utf-8')
            data = json.loads(j_data)
            
            return data['presets']
    else:
        return 'No .babelrc in the path ' + path
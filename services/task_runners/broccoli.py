import os, re

class BroccoliHandler:
    def __init__(self, path):
        """
        
        Handles single instance of Brocfile.js
        
        - self.path = path to Brocfile 
        - self.dependents = file/file types that the Brocfile handles
        
        """
        self.path = path
        self.dependents = []
        
    
    def builds_natively(self):
        """
        Checks whether Broccoli is actually used to build anything natively
        """
        os.chdir(self.path)
        
        with open('package.json', 'r') as file:
            j_data = f.read().decode('utf-8')
            data = json.loads(j_data)
                    
            if 'devDependencies' in data:
                for devDep in data['devDependencies'].iterkeys():
                    if devDep == 'broccoli-cli':
                        return True
                    
            if 'dependencies' in data:            
                for dep in data['dependencies'].iterkeys():
                    if dep == 'broccoli-cli':
                        return True
                        
        return False
import os
import fnmatch
import json 
import re

class TypeScriptHunter:
    def __init__(self, path):
        """
        Hunts for all possible instances of TypeScript in project
        """
        self.active = False
        self.extensions = {}
        self.paths = []
        self.files = []
        self.transpilations = []
        
        for root, dirs, files in os.walk(path):
            if re.search('node_modules', root) == None:
                for name in files:
                    if fnmatch.fnmatch(name, 'tsconfig.json'):
                        self.active = True
                        self.paths.append(root)
                        self.extensions[root] = []
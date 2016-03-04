import re
import os
import fnmatch

class NodeHunter:
    def __init__(self, path):
        self.path = path
            
    def find_file(self, word):
        result = []
        
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if fnmatch.fnmatch(name, word):
                    result.append({root : word})
                    
        return result
        
    def find_init_file(self):
        print self.find_file('package.json')
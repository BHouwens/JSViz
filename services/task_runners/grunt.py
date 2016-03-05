import os
import re

class GruntHunter:
    def __init__(self, path):
        os.chdir(path)
        self.active = True
        
        if os.path.isfile('Gruntfile.js'):
            self.file = open('Gruntfile.js', 'r')
        else: 
            self.active = False

    
    def find_serve(self):
        if self.active:
            with self.file as f:
                for line in f:
                    if re.search('', line):
                        return line
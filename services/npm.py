import os
import re

class NPMHunter:
    def __init__(self, path):
        os.chdir(path)
        
        if os.path.isfile('package.json'):
            self.active = True
        else:
            self.active = False
            
    def find_command(self, regex):
        """
        Searches for a given command in package.json, or False is none is found
        """
        if self.active:
            file = open('package.json', 'r') 
            with file as f:
                for line in f:
                    if re.search(regex, line):
                        command = re.search("(?<=:).+$", line)
                        return command.group(0)
                    
                return False
        else:
            return False
    
    def find_start(self):
        """
        Returns the npm start command, or False if it doesn't exist
        """
        return self.find_command('\"start\"')
            
    def find_build(self):
        """
        Returns the npm build command, or False if none exist
        """
        return self.find_command('\"build\"')
        
    def find_test(self):
        """
        Returns the npm test command, or False if none exist
        """
        return self.find_command('\"test\"')
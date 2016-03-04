import os
import re
import fnmatch

class NPMHunter:
    def __init__(self, path):
        self.packages = [] # how many entry points for npm are there?
        self.active = False
        
        for root, dirs, files in os.walk(path):
            if re.search('node_modules', root) == None:
                for name in files:
                    if fnmatch.fnmatch(name, 'package.json'):
                        self.packages.append(root)
                        self.active = True
                    
        print 'self.packages: ' + str(self.packages)
                    
            
    def find_command(self, regex):
        """
        Searches for a given command in all package.jsons, or False is none are found
        """
        packages = []
        
        if self.active:
            for dir in self.packages:
                os.chdir(dir)
                file = open('package.json', 'r') 
                
                with file as f:
                    for line in f:
                        if re.search(regex, line):
                            command = re.search("(?<=:).+$", line)
                            packages.append(command.group(0))
                        
                    return packages
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
import os, re, fnmatch

class WebpackHandler:
    def __init__(self, path):
        """
        
        Handler for a single webpack.config.js and its entry points
        
        - self.path = path to the root webpack.config.js
        - self.child_files = paths to and names of the config files entry points 
        
        """
        self.path = path
        self.child_files = []
        self.hunt_entries()
    
    def find_entry(self):
        """
        Find entry point/s for a webpack project
        """
        lines = []
        entry_found = False
        
        if os.path.isfile('webpack.config.js'):
            file = open('webpack.config.js', 'r')
            
            with file as f:
                to_continue = False
                
                for line in f:
                    if 'entry:' in line:
                        if re.search('entry\:\s*{', line) is not None:
                            # if there are multiple entry points over multiple lines
                            to_continue = True
                            continue
                        else:
                            # if there is only one entry point
                            lines.append(line)
                            break
                    
                    if to_continue:
                        if '}' not in line:
                            lines.append(line)
                        else:
                            to_continue = False
                
                return lines  
        else:
            print 'There is no webpack.config.js in the folder ' + self.path           
                            
    def set_entries(self):
        """
        Sets real entries based on the crawling done in find_entry()
        """
        entries = []
        lines = self.find_entry()
        
        for entry in lines:
            result = re.findall('(?<=\/)[a-z]+', entry)
            entries.append(result)
        
        return entries
                
   
    def hunt_entries(self):
        """
        Find all the entry files themeselves in the project.
        Is greedy, doesn't care about extensions.
        
        Example of resultant find:
            {
                'path' : 'full/path/to/file',
                'file' : 'file.js'
            }
        """
        entries = self.set_entries()
        
        for root, dirs, files in os.walk(self.path):
            for name in files:
                for entry in entries:
                    if len(entry) > 1:
                        last_dir = entry[-2]
                        
                        # checks that file is in correct dir
                        # by ensuring the last bit of the root == last
                        # bit of the entry's path
                        if last_dir in root[-len(last_dir):]:
                            if entry[-1] in name:
                                new_obj = {
                                    'path': root,
                                    'file': name
                                }
                                        
                                self.child_files.append(new_obj)
                    
                    else:
                        if entry[-1] in name:
                            new_obj = {
                                'path': root,
                                'file': name
                            }
                            
                            self.child_files.append(new_obj)
                                
        print self.child_files
                            
                        
import os, re, fnmatch

class WebpackHandler:
    def __init__(self, path):
        """
        Handler for webpack.config.js and its entry points
        """
        self.path = path
        self.child_files = []
    
    def find_entry(self):
        """
        Find entry point/s for a webpack project
        """
        self.entries = []
        lines = []
        entry_found = False
        
        os.chdir(self.path)
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
                            
    def set_entries(self):
        """
        Sets real entries based on the crawling done in find_entry()
        """
        lines = self.find_entry()
        
        for entry in lines:
            if '[' not in entry:
                result = re.findall('(?<=\/)[a-z]+(?=\'|\")', entry)
                self.entries.append(result)
            else:
                result = re.findall('(?<=\/)[a-z]+(?=\'|\")', entry)
                self.entries.append(result)
                
   
    def hunt_entries(self):
        """
        Find all the entry files themeselves in the project
        """
        self.set_entries()
        
        for root, dirs, files in os.walk(self.path):
            if re.search('node_modules', root) == None:
                for name in files:
                    for entry in self.entries:
                        for actual_entry in entry:
                            regex = r"^" + re.escape(actual_entry) + r"\.(ts|js|elm)(?!\.map)"
                            
                            if re.search(regex, name) is not None:
                                new_obj = {
                                    'path': root,
                                    'file': name
                                }
                                
                                self.child_files.append(new_obj)
                                
        print self.child_files
                            
                        
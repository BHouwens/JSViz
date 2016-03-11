import os, re

class RelationshipManager:
    def __init__(self, entries):
        """
        
        Works out the relationships between all entry points
        and their descendants
        
        - self.entries = list of entry point dicts
        
        """
        self.entries = entries
        self.families = []
        self.find_dependencies()
        
    def find_dependencies(self):
        
        for entry in self.entries:
            children = entry['children']
            
            for details in children:
                family = {
                    'parent' : details['file']
                }
                
                path = os.path.join(details['path'], details['file'])
            
                with open(path, 'r') as file:
                    for line in file:
                        if re.search('import', line) is not None or re.search('require', line) is not None:
                            if re.search('.\/', line) is not None:
                                print line
                     
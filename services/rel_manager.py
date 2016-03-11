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
        self.find_import_dependencies()
        print self.families
        
    def find_import_dependencies(self):
        """
        Find all strictly imported dependencies for each file and create a "family" with them.
        
        Structure of a family is such:
        
        family = {
            'parent' : parent file for later reference,
            'externals' : list of "external" imports, such as angular or jquery,
            'internals' : list of "internal" imports, those created in this specific project
        }
        """
        for entry in self.entries:
            children = entry['children']
            
            for details in children:
                family = {
                    'parent' : details['file'],
                    'externals' : [],
                    'internals' : []
                }
                
                path = os.path.join(details['path'], details['file'])
            
                with open(path, 'r') as file:
                    for line in file:
                        if re.search('import', line) is not None or re.search('require', line) is not None:
                            # if it's an internal import
                            if re.search('.\/', line) is not None:
                                if re.search('\"', line) is not None:
                                    substring = self.capture_substring('"', line)
                                    family['internals'].append(substring)
                                elif re.search('\'', line) is not None:
                                    substring = self.capture_substring('\'', line)
                                    family['internals'].append(substring)
                            # if it's an external import    
                            else:
                                if re.search('\"', line) is not None:
                                    family['externals'].append(self.capture_substring('"', line))
                                elif re.search('\'', line) is not None:
                                    family['externals'].append(self.capture_substring('\'', line))
                                
                    self.families.append(family)
                    
                    
    def capture_substring(self, char, line):
        """
        Returns a substring of a string contained between two entries of char
        """
        indices = [i for i, letter in enumerate(line) if letter == char]
        substring = line[indices[0] + 1: indices[1]]
        
        return substring
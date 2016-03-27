import os
import re
import fnmatch

class Networker:
    def __init__(self, path, extensions):
        """
        Works out the relationships between all generic files, creating a network.
        This will then be used to build the 'files' and 'links' data for D3
        """
        
        self.files = []
        self.links = []
        
        self.path = path
        self.extensions = extensions
        self.id = 0
        self.check_templates = False
        
    def build_file_list(self):
        """
        Build list of files throughout the project
        """
        
        for root, dirs, files in os.walk(self.path):
            if re.search('node_modules', root) == None and re.search('dist', root) == None:
                for name in files:
                    for extension in self.extensions:
                        if fnmatch.fnmatch(name, extension):
                            self.files.append({
                                'name': name,
                                'path': root,
                                'id': self.id
                            })
                            
                            self.id += 1
                            
    def find_dependents(self):
        """
        Finds all dependents for each file and adds to the list.
        Runs self.find_imports and loops over to find dependents
        """
        
        self.find_imports()
        
        for file in self.files:
            name = file['name']
            file['dependents'] = []
            
            for neighbour in self.files:
                for imports in neighbour['imports']:
                    if imports is not None:
                        if self.name_match(name, imports) and self.path_match(file['path'], imports):
                            file['dependents'].append(neighbour['name'])
                            self.links.append({'source': file['id'], 'target': neighbour['id']})
                
    
    def find_imports(self):
        """
        Finds all imports for each file and adds to the list
        """
        
        self.build_file_list()
        
        for file in self.files:
            entry = open(os.path.join(file['path'], file['name']), 'r')
            file['imports'] = []
             
            with entry as f:
                for line in entry:
                    if 'import' in line or 'require' in line:
                        file['imports'].append(self.rip_import(line))
                        
                    if self.check_templates:
                        if 'src=' in line:
                            files['imports'].append(self.rip_import(line))
                        
    def rip_import(self, line):
        """
        Rips the imported dependencies from a line
        """
        
        if '\'' in line:
            indices = [i for i, char in enumerate(line) if char == '\'']
            return line[indices[-2] + 1: indices[-1]]
        elif '\"' in line:
            indices = [i for i, char in enumerate(line) if char == '\"']
            return line[indices[-2] + 1: indices[-1]]


    def name_match(self, name, imported):
        """
        Performs a greedy match between a file and its potential import's name
        """
        
        dot_indices = [i for i, char in enumerate(name) if char == '.']
        searchable_name = name[:dot_indices[-1]]
        
        return searchable_name in imported
        
        
    def path_match(self, path, imported):
        """
        Performs a greedy match between a file and its potential import's path
        """
        
        indices = [i for i, char in enumerate(imported) if char == '/']
        if len(indices) > 0:
            imported = imported[1:indices[-1]]
            
        return imported in path
        
        
    def check_for_templates(self):
        """
        Checks whether system requires template files to be searched
        """
        
        template_extensions = ['*.html', '*.haml', '*.jade', '*.ejs']
        
        for extension in template_extensions:
            if extension in self.extensions:
                self.check_templates = True
                break
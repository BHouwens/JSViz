import os
import re
import fnmatch
from py_import import PythonImportHandler

import_handler = PythonImportHandler()

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
            if re.search('venv', root) == None and re.search('node_modules', root) == None:
                for name in files:
                    for extension in self.extensions:
                        if fnmatch.fnmatch(name, extension):
                            extension_class = extension.replace('*.', '')
                            
                            self.files.append({
                                'name': name,
                                'path': root,
                                'id': self.id,
                                'class': extension_class
                            })
                            
                            self.id += 1
                      
    def find_imports(self):
        """
        Finds all imports for each file and adds to the list
        """
        
        self.build_file_list()
        self.check_for_templates()
        
        for file in self.files:
            entry = open(os.path.join(file['path'], file['name']), 'r')
            file['imports'] = []
             
            with entry as f:
                for line in entry:
                    possible_import = import_handler.find_import(line, file['path'], self.path)
                    if possible_import:
                        file['imports'].append(possible_import)
                            
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
                        if imports['path'] == file['path'] and imports['file'] == file['name']:
                            file['dependents'].append(neighbour['name'])
                            self.links.append({'source': file['id'], 'target': neighbour['id']})
        
    def cull(self):
        """
        Culls orphan and widow nodes if the number of nodes is very high.
        This keeps the visualisation uncluttered and legible
        """

        print(self.files)
        if len(self.files) > 200:
            self.files = [node for node in self.files if len(node['imports']) == 0 and len(node['dependents']) == 0]

        
    def check_for_templates(self):
        """
        Checks whether system requires template files to be searched
        """
        
        template_extensions = ['*.html', '*.haml', '*.jade', '*.ejs']
        
        for extension in template_extensions:
            if extension in self.extensions:
                self.check_templates = True
                break
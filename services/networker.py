import os
import re
import fnmatch
from js_import import check as js_condition

class Networker:
    def __init__(self, path, extensions):
        """
        Works out the relationships between all generic files, creating a network.
        This will then be used to build the 'files' and 'links' data for D3
        """
        
        self.files = []
        self.links = []
        
        self.path = path
        self.condition = js_condition
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
                            extension_class = extension.replace('*.', '')
                            
                            self.files.append({
                                'name': name,
                                'path': root,
                                'id': self.id,
                                'class': extension_class
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
                        if imports['path'][-1] == '/':   
                            double_slash = True
                        else:
                            double_slash = False
                            
                        path_to_check = self.path_joins(imports['path'], file['name'], double_slash)
                        
                        # if it's a file
                        if os.path.exists(path_to_check):
                            if imports['path'] == file['path'] and imports['file'] in file['name']:
                                file['dependents'].append(neighbour['name'])
                                self.links.append({'source': file['id'], 'target': neighbour['id']})
                                
                        # if it's a folder
                        
                        
    
    def find_imports(self):
        """
        Finds all imports for each file and adds to the list
        """
        
        self.build_file_list()
        self.check_for_templates()
        
        char_list = ['\'', '\"']
        
        for file in self.files:
            entry = open(os.path.join(file['path'], file['name']), 'r')
            file['imports'] = []
             
            with entry as f:
                for line in entry:
                    if self.condition(line):
                        file['imports'].append(self.rip_import(char_list, line, file['path']))
                        
                    if self.check_templates:
                        if 'src=' in line:
                            file['imports'].append(self.rip_import(char_list, line, file['path']))
                        
    def rip_import(self, char_list, line, path):
        """
        Rips the imported dependencies from a line
        """
        
        for char in char_list:
            if char in line:
                indices = [i for i, c in enumerate(line) if c == char]
                actual_import = line[indices[-2] + 1: indices[-1]]
                
                return self.determine_file(line, actual_import, path)
            
            
    def determine_file(self, line, actual_import, path):
        """
        Determines the path and actual file of the import
        """
    
        if '/' in actual_import:
            indices = [i for i, char in enumerate(actual_import) if char == '/']
            import_file = actual_import[indices[-1] + 1:]
            import_path = actual_import[:indices[-1]]
            
            if actual_import[:2] == './':
                return {
                    'path': '/'.join([ path, actual_import[2:indices[-1]] ]),
                    'file': import_file,
                    'line': line
                }
            
            if actual_import[:2] == '..':
                jump_ups = len(re.findall('\.\.', actual_import))
                path = path.split('/')
                
                for i in range(jump_ups):
                    del path[-1]
                    import_path = import_path[3:]
                    
                return {
                    'path': '/'.join(['/'.join(path), import_path]),
                    'file': import_file,
                    'line': line
                }
        
        else:
            return {
                'path': path,
                'file': actual_import,
                'line': line
            }
        
        
    def check_for_templates(self):
        """
        Checks whether system requires template files to be searched
        """
        
        template_extensions = ['*.html', '*.haml', '*.jade', '*.ejs']
        
        for extension in template_extensions:
            if extension in self.extensions:
                self.check_templates = True
                break
                
    def get_import(self, line):
        """
        Get imported function/variable from line
        """
        
        if len(re.findall('{', line)) > 0:
            opening = line.index('{')
            closing = line.index('}')
            
            return line[opening + 1:closing]
                
    def path_joins(self, first_join, second_join, condition=True):
        """
        Will determine kind of join based on condition
        """
        
        if condition:
            return ''.join([ first_join, second_join ])
        else:
            return '/'.join([ first_join, second_join ])
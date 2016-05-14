import re
import os

class PythonImportHandler:
    
    def __init__(self):
        self.line = '';
        self.path = '';
        self.core_path = '';
        self.externals = []
    
    def find_import(self, line, path, core_path):
        """
        Entry method. Finds the file by calling internal processing method
        depending on the kind of import
        """
        
        self.line = line
        self.path = path
        self.core_path = core_path
        
        if re.search(r'^from\s', line) is not None and re.search(r'\simport\s', line) is not None:
            return self.process_import(r'(?<=from\s)[\s\_\.a-zA-Z0-9]+', 'from')
                    
        elif re.search(r'^import\s', line) is not None:
            return self.process_import(r'(?<=import\s)[\_\.a-zA-Z0-9]+', 'import')
            
        else:
            return False
            
            
    def process_import(self, regex, type):
        """
        Processes the import line and finds the file needed
        """
        
        imported = re.search(regex, self.line).group(0)
        import_list = filter(None, imported.split('.'))
        possible_file = None
        
        # munge the 'from' line for import and possible file
        if type == 'from':
            for entry in import_list:
                if 'import' in entry:
                    new_list = entry.split('import')
                    import_list[-1] = re.sub(r'\s', '', new_list[0])
                    possible_file = re.sub(r'\s', '', new_list[1])
                    break
            
        new_path = '/'.join([self.path, '/'.join(import_list)])
        
        # check from current dir 
        check_from_current_path = self.walk_through_and_find_file(new_path, import_list, possible_file)    
        if check_from_current_path:
            return check_from_current_path
        
        # if nothing found, check from original path up
        check_from_core_path = self.check_from_core_path(import_list, possible_file)
        if check_from_core_path:
            return check_from_core_path
            
        return False
        
        
    def walk_through_and_find_file(self, new_path, import_list, possible_file):
        """
        Walks through the project from the provided new_path and 
        retroactively looks for the needed file
        """
        
        import_list_length = len(import_list)
        
        while import_list_length > 0:
            # if it's a 'from' line
            if possible_file is not None and os.path.exists( '.'.join( ['/'.join([new_path, possible_file]), 'py'] ) ):
                return {
                    'path': new_path,
                    'file': '.'.join([possible_file, 'py'])
                }  
            # if it's a straight import line 
            else:
                if os.path.exists('.'.join([new_path, 'py'])):
                    indices = [i for i, char in enumerate(new_path) if char == '/']
                    return {
                        'path': new_path[:indices[-1]],
                        'file': '.'.join([new_path[indices[-1] + 1:], 'py'])
                    }
                else:
                    new_path = '/'.join([self.path, '/'.join(import_list[:import_list_length])])
                    import_list_length -= 1
        
        return False
        
        
    def check_from_core_path(self, import_list, possible_file):
        """
        Checks for file starting from the core_path
        """
        
        path_list = self.core_path.split('/')
        
        if path_list[-1] == import_list[0]:
            indices = [i for i, char in enumerate('/'.join(path_list)) if char == '/']
            new_path = '/'.join([ '/'.join( path_list[:indices[-1]] ), '/'.join( import_list ) ])
            
            check_from_core_path = self.walk_through_and_find_file(new_path, import_list, possible_file)
            if check_from_core_path:
                return check_from_core_path
            return False
        elif import_list[0] not in self.externals:
                self.externals.append(import_list[0])
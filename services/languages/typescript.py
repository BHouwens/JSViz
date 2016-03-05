import os, fnmatch, json, re

class TypeScriptHunter:
    def __init__(self, path):
        """
        Hunts for all possible instances of TypeScript in project
        """
        self.active = False
        self.extensions = {}
        self.paths = []
        self.files = []
        
        for root, dirs, files in os.walk(path):
            if re.search('node_modules', root) == None:
                for name in files:
                    if fnmatch.fnmatch(name, 'tsconfig.json'):
                        self.active = True
                        self.paths.append(root)
                        self.extensions[root] = []
    
    def crawl_tsd(self):
        """
        Crawls through all instances of tsd.json and find extensions
        """
        for path in self.paths:
            os.chdir(path)
            with open('tsd.json', 'r') as file:
                json_data = file.read().decode('utf-8')
                data = json.loads(json_data)
                
                for k, v in data.iteritems():
                    if k == 'installed':
                        for child_k, child_v in v.iteritems():
                            self.extensions[path].append(re.search("[a-z]+\/", child_k).group(0)[:-1])
                            
    def crawl_tsconfig(self):
        """
        Crawls through all instances of tsconfig.json and finds compiler options and files etc
        """
        for path in self.paths:
            os.chdir(path)
            with open('tsconfig.json', 'r') as file:
                json_data = file.read().decode('utf-8')
                data = json.loads(json_data)
                
                for k, v in data.iteritems():
                    if k == 'files':
                        self.files = v
                            
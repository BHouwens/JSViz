import os, fnmatch, json, re

class NpmHandler:
    def __init__(self, path):
        """
        
        Handles a single package.json file and its task runners, dependencies
        and languages
        
        """
        self.active = False
        self.path = path
        
        self.possible_task_runners = {
            'grunt' : "Gruntfile.js",
            'webpack' : "webpack.config.js",
            'broccoli': "Brocfile.js",
            'gulp' : "Gulpfile.js",
            'cake' : "Cakefile"
        }
        
        self.possible_languages = [
            'typescript',
            'elm'
        ]
        
        os.chdir(self.path)
        if os.path.isfile('package.json'):
            self.active = True
        else:
            print 'There is no package.json in path ' + self.path
        
    def find_everything(self):
        """
        Collect and establish what each package.json in a project brings in terms
        of languages and task runners
        """
        self.find_task_runners()
        self.find_languages()
        
    def find_languages(self):
        """
        Finds all languages that this package.json allows you to use
        """
        self.languages = {}
        
        if self.active:
            current_lang = '' 
            file = open('package.json', 'r')
                
            with file as f:
                json_data = f.read().decode('utf-8')
                data = json.loads(json_data)
                    
                if 'devDependencies' in data:
                    for devDep in data['devDependencies'].iterkeys():
                        for language in self.possible_languages:
                            if language in devDep and language != current_lang:
                                self.languages[dir].append(language) 
                                current_lang = language
                    
                if 'dependencies' in data:            
                    for dep in data['dependencies'].iterkeys():
                        for language in self.possible_languages:
                            if language in dep and language != current_lang:
                                self.languages[dir].append(language) 
                                current_lang = language
        
    def find_task_runners(self):
        """
        Will find task runner/s in this package.json
        """
        self.dep_task_runners = {}
        
        if self.active:
            current_runner = ''
            
            for dir in self.packages:
                os.chdir(dir)
                file = open('package.json', 'r')
                
                self.dep_task_runners[dir] = []
                
                with file as f:
                    json_data = f.read().decode('utf-8')
                    data = json.loads(json_data)
                    
                    if 'devDependencies' in data:
                        for devDep in data['devDependencies'].iterkeys():
                            for runner, lookup in self.possible_task_runners.iteritems():
                                if runner in devDep and runner != current_runner:
                                    self.dep_task_runners[dir].append({runner: lookup}) 
                                    current_runner = runner
                    
                    if 'dependencies' in data:                                
                        for dep in data['dependencies'].iterkeys():
                            for runner, lookup in self.possible_task_runners.iteritems():
                                if runner in dep and runner != current_runner:
                                    self.dep_task_runners[dir].append({runner: lookup})  
                                    current_runner = runner
                                    
                current_runner = ''
            
    def find_command(self, regex):
        """
        Searches for a given command in all package.jsons, or False is none are found
        """
        packages = []
        
        if self.active:
            current_call = ''
            
            for dir in self.packages:
                os.chdir(dir)
                file = open('package.json', 'r') 
                
                with file as f:
                    json_data = file.read().decode('utf-8')
                    data = json.loads(json_data)
                    
                    for call, command in data['scripts'].iteritems():
                        if re.search(regex, call) is not None and current_call != call:
                            packages.append({
                                'path' : dir,
                                'call' : call,
                                'command' : command
                            })
                            
                            # prevents duplicates
                            current_call = call
                            
                    current_call = ''    
                    return packages
        else:
            return False
            
    def set_starts(self):
        """
        Sets all start commands for this class instance
        """
        self.starts = self.find_command('start')
        
    def set_devs(self):
        """
        Sets all dev commands for this class instance
        """
        self.devs = self.find_command('dev')
            
    def find_build(self):
        """
        Returns the npm build command, or False if none exist
        """
        return self.find_command('build')
        
    def find_test(self):
        """
        Returns the npm test command, or False if none exist
        """
        return self.find_command('test')
import re

from task_runners.npm import NPMHunter

class Controller:
    def __init__(self, path):
        self.path = path
        self.npm = NPMHunter(self.path)
        
        # individual task runners, their full commands, and their init files (such as webpack.config.js)
        self.task_runners = {}
        
        self.possible_task_runners = {
            'grunt' : {'regex': "grunt", 'file': "Gruntfile.js"},
            'webpack' : {'regex': "webpack", 'file': "webpack.config.js"},
            'node' : {'regex': "node", 'file': "[a-z]+.js"},
            'broccoli': {'regex': "broccoli", 'file': "Brocfile.js"},
            'gulp' : {'regex': "gulp", 'file': "Gulpfile.js"},
            'cake' : {'regex': "cake", 'file': "Cakefile"}
        }
    
    def collect_task_runners(self):
        """
        Collects all task runners in project, as well as their respective commands
        """
        
        # If package.jsons exist
        if self.npm.active:
            id = 0
            start_commands = self.npm.find_start()
            
            for command in start_commands: 
                for task_runner, value in self.possible_task_runners.iteritems():
                    if re.search(value['regex'], command) is not None:
                    
                        self.task_runners[id] = {
                            'task_runner' : task_runner,
                            'command' : command
                        }
                        
                        id += 1
                        
                        if task_runner == 'node':
                            self.task_runners['file_to_find'] = re.search(value['file'], command).group(0)
                        else:
                            self.task_runners['file_to_find'] = value['file']
                        
            print 'task runners: ' + str(self.task_runners)
        # If task runners are called directly
        else:
            for root, dirs, files in os.walk(self.path):
                if re.search('node_modules', root) == None:
                    for task_runner, value in self.possible_task_runners.iteritems():
                        for name in files:
                            if fnmatch.fnmatch(name, task_runner):
            
    def get_task_runners(self):
        """
        Returns all task runners as a dict. Only used for testing
        """
        self.collect_task_runners()
        return self.task_runners

    def find_init_files(self):
        """
        Finds all the initialisation files that npm starts
        """
        self.get_task_runners()
        
        if self.task_runners:
            for id, command_obj in self.task_runners.iteritems():
                if command_obj['task_runner'] == 'node':
                    self.init_files[id] = re.search(command_obj['file_to_find'], command_obj['command']).group(0)
                else:
                    self.init_files[id] = command_obj['file_to_find']
                   
                    
    def get_init_files(self):
        """
        Returns all initialisation files. Only to be used for testing
        """
        self.find_init_files()
        print 'init_files: ' + str(self.init_files)
                
                    
                           
            
            
        
        
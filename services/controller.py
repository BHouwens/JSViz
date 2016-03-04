import re

from npm import NPMHunter
from grunt import GruntHunter
from node import NodeHunter

class Controller:
    def __init__(self, path):
        self.path = path
        self.npm = NPMHunter(self.path)
        self.task_runner = 'none'
        self.possible_task_runners = {
            'grunt' : "grunt",
            'webpack' : "webpack",
            'node' : "node"
        }
    
    def get_task_runner(self):
        if self.npm.active:
            start_command = self.npm.find_start()
            
            for key, value in self.possible_task_runners.iteritems():
                if re.search(value, start_command) is not None:
                    self.task_runner = key
                    return self.task_runner
                    
            return self.task_runner
        else:
            return self.task_runner

    def find_init_file(self):
        print self.task_runner
        
        if self.task_runner == 'webpack':
            self.handler = WebpackHunter()
            self.init_file = 'webpack.config.js'
            
        elif self.task_runner == 'grunt':
            self.handler = GruntHunter()
            self.init_file = 'Gruntfile.js'
            
        elif self.task_runner == 'node':
            self.handler = NodeHunter(self.path)
            self.init_file = self.handler.find_init_file()
            
            
        
        
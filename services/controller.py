import os, re

from task_runners.npm import NpmHandler
from task_runners.webpack import WebpackHandler

class Controller:
    def __init__(self, path):
        """
        
        Main controller/handler for the whole system.
        
        - self.path = path to treat as project root
        - self.task_runners = actual task runners used in project
        - self.npm = npm handler object for package.json
        
        """
        self.path = path
        self.task_runners = []
        self.npm = NpmHandler(self.path)
        
        # do preliminary search through package.jsons
        # this will cut down work later
        if self.npm.active:
            self.npm.find_everything()
            self.actual_task_runners()
            print 'actual task runners: ' + str(self.task_runners)
            
    def find_init_files(self):
        self.npm.set_starts()
        
        if len(self.npm.starts) == 0:
            self.npm.set_devs()
            print 'devs: ' + str(self.npm.devs)   
        else:
            print 'starts: ' + str(self.npm.starts)
        
    def actual_task_runners(self):
        """
        Separates runners that are simply installed from ones that are
        actually being used
        """
        if self.npm.task_runners:
            for entry in self.npm.task_runners:
                for runner, main_file in entry.iteritems():
                    for root, dir, files in os.walk(self.path):
                        if 'node_modules' not in root:
                            for name in files:
                                if name == main_file:
                                    self.task_runners.append({
                                        'path': root,
                                        'runner': runner,
                                        'file': main_file
                                    })
                                
                
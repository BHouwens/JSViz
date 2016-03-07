import os, re
from task_runners.npm import NPMHunter
from task_runners.webpack import WebpackHandler

class Controller:
    def __init__(self, path):
        self.path = path
        self.task_runners = {}
        self.npm = NPMHunter(self.path)
        
        # do preliminary search through package.jsons
        # this will cut down work later
        if self.npm.active:
            self.npm.find_everything()
            self.actual_task_runners()
            
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
        if self.npm.dep_task_runners:
            
            for path, detail in self.npm.dep_task_runners.iteritems():
                os.chdir(path)
                
                for entry in detail:
                    (k, v), = entry.items()
                    
                    if os.path.isfile(v):
                        self.task_runners[path] = k
                    
                                
                
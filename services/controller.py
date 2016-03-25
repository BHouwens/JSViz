import os, re

from task_runners.npm import NpmHandler
from task_runners.webpack import WebpackHandler
from rel_manager import RelationshipManager

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
        self.handlers = []
        self.npm = NpmHandler(path)
        
        # D3 vars
        self.nodes = []
        self.links = []
        self.id = 0
        
        # do preliminary search through package.jsons
        # this will cut down work later
        if self.npm.active:
            self.npm.find_everything()
            self.actual_task_runners()
            self.handle_task_runner()
            self.munge_data()

    def handle_task_runner(self):
        """
        Handles task runners and their child files appropriately
        
        Creates list with dicts of structure:
        
            {
                'children': [
                    {
                        'file': filename,
                        'path': full/path/to/file
                    }
                ],
                'parent': task runner file
                'path': path to task runner file
            }    
        """
        handler_entry = {
            'path' : self.path
        }
        
        for entry in self.task_runners:
            if entry['runner'] == 'webpack':
                handler = WebpackHandler(self.path)
                handler_entry['parent'] = 'webpack.config.js'
                handler_entry['children'] = handler.child_files
            
                self.handlers.append(handler_entry)
        
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
        
    def munge_data(self):
        for entry in self.handlers:
            node = {'file': entry['parent'], 'id': self.id}
            self.nodes.append({'file': node['file'], 'class': 'handler'})
            
            for child_file in entry['children']:
                self.id += 1
                self.nodes.append({'file': child_file['file'], 'class': 'dependency'})
                self.links.append({'source': node['id'], 'target': self.id})
                
              
            
              
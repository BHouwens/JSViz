

class NodeHandler:
    def __init__(self, path, file, middleware = None):
        """
        
        Handles a single instance of Node in a project
        
        - self.path = path to the Node server file
        - self.middleware = middleware for the server (eg. Express)
        - self.file = Node server file
        
        """
        self.path = path
        self.middleware = middleware
        self.file = file
        
    def find_routes(self):
        if self.middleware == 'express':
            for root, dir, files in os.walk(self.path):
                for name in file
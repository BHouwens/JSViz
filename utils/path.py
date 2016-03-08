def path_handler(path):
    """
    Returns prettified path
    """
    if path[:7] == '/Users/':
        stripped_path = path[7:]
        idx = stripped_path.find('/')
        
        return stripped_path[idx + 1:]
    
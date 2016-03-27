def check(line):
    if 'import' in line or 'require' in line:
        return True
    else:
        return False
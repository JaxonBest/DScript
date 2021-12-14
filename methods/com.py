# Comment a line
def com(command, ln) -> str:
    return '# {}'.format(' '.join(x for x in command['args']))
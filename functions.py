import _print

def die(message=None):
    if message is not None:
        _print.warning(str(message))
    exit(0)

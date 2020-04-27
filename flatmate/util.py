def format_args(*args, **kwargs):
    args_repr = [repr(x) for x in args]
    kwargs_repr = [name + '=' + repr(value) for name, value in kwargs.items()]
    return ', '.join(args_repr + kwargs_repr)

def echo(func):
    """Print the name and arguments on each call of the decorated function.

    Example:
        @flatmate.echo
        def OnMidiMsg(event):
            pass
    """
    def wrap(*args, **kwargs):
        print("Called: {}({})".format(func.__name__, format_args(*args, **kwargs)))
        return func(*args, **kwargs)
    return wrap

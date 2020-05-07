# https://github.com/praashie/flatmate

from . import util

class Chain:
    """Container for chaining functions together

    Args:
        *funcs: zero or more functions.
        stop_function: stop condition function

    When invoking the function chain, stop_function is called with
    (last_result, *args, **kwargs), where:
        last_result: Return value of the previous chain function call
        *args, **kwargs: Arguments supplied to Chain.__call__()

    Example:
        >>> printfunc = lambda s: lambda: print(s)
        >>> c = Chain()
        >>> c.attach(printfunc("hello"), printfunc("world"))
        >>> c.attach(printfunc("first!"), before=True)
        >>> c()
        first!
        hello
        world
    """

    def __init__(self, *funcs, stop_function=None):
        self.callbacks = list(funcs)
        self.stop_function = stop_function
        self.last_result = None
        self.verbose = False

        self.__name__ = Chain.__name__

    def __call__(self, *args, **kwargs):
        if self.verbose:
            print("{}({})".format(self.__name__, util.format_args(*args, **kwargs)))

        for f in self.callbacks:
            self.last_result = f(*args, **kwargs)
            if self.stop_function and self.stop_function(self.last_result, *args, **kwargs):
                break
        return self.last_result

    def attach(self, *funcs, before=False):
        """Attach new functions to be called in sequence

        Args:
            before: if True, attach functions before existing ones.
        """

        if before:
            self.callbacks = list(funcs) + self.callbacks
        else:
            self.callbacks.extend(funcs)
        return self

def eventHandled(_, event):
    return event.handled

def EventChain(*funcs):
    """Function chain that stops when the given event is handled"""
    return Chain(*funcs, stop_function=eventHandled)

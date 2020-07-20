# https://github.com/praashie/flatmate

from . import util
from .profiling import Profiler

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
        self.profiler = None

        self.__name__ = Chain.__name__

    def __call__(self, *args, **kwargs):
        if self.profiler is not None:
            self.profiler.start()

        if self.verbose:
            print("{}({})".format(self.__name__, util.format_args(*args, **kwargs)))

        for f in self.callbacks:
            self.last_result = f(*args, **kwargs)
            if self.stop_function and self.stop_function(self.last_result, *args, **kwargs):
                break

        if self.profiler is not None:
            self.profiler.stop()

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

    def startProfiling(self):
        if not self.profiler:
            self.profiler = Profiler(self.__name__)
        else:
            self.profiler.reset()

def eventHandled(_, event):
    return event.handled

def EventChain(*funcs):
    """Function chain that stops when the given event is handled"""
    return Chain(*funcs, stop_function=eventHandled)

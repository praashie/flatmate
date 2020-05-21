# https://github.com/praashie/flatmate

import device
from . import util
from . import flags

def SimpleSnippet(target_function_name):
    """Wrap a function for including with Hooker"""
    def _SimpleSnippet(func):
        s = util.Empty()
        setattr(s, target_function_name, func)
        s.__name__ = func.__name__
        s.__doc__ = func.__doc__
        return s
    return _SimpleSnippet

class TranslateCCBase:
    """Replace/clone a CC message with another CC number."""
    def __init__(self, cc_source, cc_target, clone=False):
        self.cc_source = cc_source
        self.cc_target = cc_target
        self.clone = clone

    def OnMidiIn(self, event):
        if event.controlNum == self.cc_source:
            event.data1 = self.cc_target
            device.processMIDICC(event)
            if self.clone:
                event.data1 = self.cc_source
                event.handled = False
            else:
                event.handled = True

def void(event):
    """Mark event as handled without action"""
    event.handled = True

def EventDumper(s='', attrs=None):
    """Create a named dumper for FL event data"""
    def _EventDumper(event):
        print("{}: {}".format(s, util.repr_attrs(event, attrs=attrs)))
        print("pmeFlags: " + flags.PME(event.pmeFlags))
    return _EventDumper

@SimpleSnippet("OnRefresh")
def refreshDumper(refresh_flags):
    """Print flags activated from OnRefresh"""
    print("OnRefresh({})".format(flags.HW_Dirty(refresh_flags)))

def GenericDumper(name="GenericDumper"):
    """Create a dumper that prints any arguments it receives"""
    def _dumper(*args, **kwargs):
        print("{}({})".format(name, util.format_args(*args, **kwargs)))
    return _dumper

def process(event):
    """Pass all events to device.processMIDICC"""
    device.processMIDICC(event)
    print("After: " + util.repr_attrs(event))

sustainFix = TranslateCCBase(0x40, 0x3F, clone=True)
sustainFix.__doc__ = """Copy sustain CC to 0x3F so both VST and native plugins handle it"""


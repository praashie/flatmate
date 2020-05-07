import device
from . import util
from . import flags

class TranslateCCBase:
    def __init__(self, cc_source, cc_target, clone=False):
        """Replace/clone a CC message with another CC number."""
        self.cc_source = cc_source
        self.cc_target = cc_target
        self.clone = clone

    def OnControlChange(self, event):
        if event.controlNum == self.cc_source:
            if self.clone:
                device.processMIDICC(event)
            event.controlNum = self.cc_target

            event.handled = True

def Void(event):
    """Mark event as handled without action"""
    event.handled = True

def EventDump(s='', attrs=None):
    def _EventDump(event):
        print("{}: {}".format(s, util.repr_attrs(event, attrs=attrs)))
        print("pmeFlags: " + flags.PME(event.pmeFlags))
    return _EventDump

class OnRefreshDump:
    def OnRefresh(refresh_flags):
        print("OnRefresh({})".format(flags.HW_Dirty(refresh_flags)))

def GenericDump(name="GenericDump"):
    def _dumper(*args, **kwargs):
        print("{}({})".format(name, util.format_args(*args, **kwargs)))
    return _dumper

def Process(event):
    device.processMIDICC(event)
    print("After: " + util.repr_attrs(event))

SustainFix = TranslateCCBase(0x40, 0x3F, clone=True)


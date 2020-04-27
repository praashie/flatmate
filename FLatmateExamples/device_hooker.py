# name=FLatmate Hooker Example
# url=

from flatmate import Hooker
Hooker.setVerbose()

last_event = None

def OnMidiMsg(event):
    global last_event
    last_event = event

Hooker.install(globals())

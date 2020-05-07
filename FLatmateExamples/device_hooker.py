# name=FLatmate Hooker Example
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=227405

from flatmate.hooker import Hooker
Hooker.setVerbose()

last_event = None

def OnMidiMsg(event):
    global last_event
    last_event = event

Hooker.install(globals())

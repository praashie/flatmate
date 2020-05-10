# name=FLatmate throttled MIDI capture
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=227405

from flatmate.hooker import *
from flatmate import snippets

print(
"""
FLatmate throttled MIDI capture
--------------------------------

All MIDI input is currently blocked.
To display and pass the next 5 messages through, enter:

captures = 5


"""
)

captures = 0

@Hooker.OnMidiIn.attach
def limit_messages(event):
    global captures
    if captures > 0:
        captures -= 1
    else:
        event.handled = True

Hooker.OnMidiIn.attach(snippets.EventDumper("OnMidiIn"))

# name=FLatmate Hooker Example 2
# url=https://github.com/praashie/flatmate

from flatmate.hooker import *
from flatmate import snippets

@Hooker
def OnInit():
    print("Yay!")

@Hooker.OnDeInit.attach
def test():
    print("Not cool.")

dump_events = ['OnMidiIn', 'OnMidiMsg', 'OnNoteOn', 'OnControlChange']
for d in dump_events:
    Hooker.chains[d].attach(snippets.EventDump(d))

Hooker.OnNoteOn.attach(snippets.Process)
Hooker.include(snippets.SustainFix)

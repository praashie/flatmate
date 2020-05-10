# name=FLatmate snippets example
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=227405

from flatmate.hooker import *
from flatmate import snippets

# Use Hooker.include() for snippets with specific behavior
Hooker.include(snippets.refreshDumper)
Hooker.include(snippets.sustainFix)

# Hooker.EntryPoint.attach() is used to attach a function to a specific entry point.
Hooker.OnNoteOn.attach(snippets.EventDumper("Note on"))

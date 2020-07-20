# Access DAW integration using any MIDI keyboard.

from time import time

import device
import midi
import transport
import ui
import utils

from .control import MIDIControl
from .hooker import Hooker
from . import icons

class SustainPedalActivator:
    def __init__(self, channel, timeout=0.4, count=3):
        self.timeout = timeout
        self.count_required = count
        self.last_press = None

        self.pedal = MIDIControl(channel, 64)
        self.pedal.set_callback(self.onPedal)

    def onPedal(self, pedal, event):
        state = pedal.value > 0x3F
        last_state = pedal.value_previous > 0x3F
        high_edge = state > last_state
        low_edge = state < last_state
        if high_edge:
            t = time()
            if (t - (self.last_press or 0)) > self.timeout:
                self.count = 0
            self.count += 1
            self.last_press = t
            if self.count == self.count_required:
                Alakazam.activate()
        elif low_edge:
            Alakazam.deactivate()

class AlakazamBase:
    def __init__(self):
        self.activated = False
        self.onActivated = None
        self.onDeactivated = None

    def activate(self):
        ui.setHintMsg(icons.eye + icons.eye + "Alakazam!")
        self.activated = True
        if callable(self.onActivated):
            self.onActivated(self)

    def deactivate(self):
        ui.setHintMsg("")
        if self.activated:
            self.activated = False
            if callable(self.onDeactivated):
                self.onDeactivated(self)

    noteMap = {
        "F": (midi.FPT_Escape, "Esc"),
        "F#": (midi.FPT_No, "No"),
        "G": (midi.FPT_Enter, "Enter"),
        "G#": (midi.FPT_Yes, "Yes"),
        "A": (midi.FPT_Left, "Left"),
        "A#": (midi.FPT_Up, "Up"),
        "B": (midi.FPT_Down, "Down"),
        "C": (midi.FPT_Right, "Right")
    }

    def handleNote(self, event, state):
        noteIndex = event.note % 12
        noteName = utils.NoteNameT[noteIndex]

        if noteName in self.noteMap:
            action, description = self.noteMap[noteName]
            transport.globalTransport(action, state * 1, event.pmeFlags)
            ui.setHintMsg(icons.eye + icons.eye + "Alakazam: " + description)
        event.handled = True

    def OnNoteOn(self, event):
        if self.activated:
            self.handleNote(event, True)

    def OnNoteOff(self, event):
        if self.activated:
            self.handleNote(event, False)

Alakazam = AlakazamBase()
Hooker.include(Alakazam)

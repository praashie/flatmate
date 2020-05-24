# https://github.com/praashie/flatmate

import device
import midi

from .event import RECEvent

DEFAULT_PORT = device.getPortNumber()

class MIDIControl:
    def __init__(self, channel, ccNumber, port=DEFAULT_PORT, name='', **kwargs):
        self.channel = channel
        self.ccNumber = ccNumber
        self.port = port
        self.name = name
        self.value = 0
        self.value_previous = 0

        self.verbose = False

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def set_callback(self, callback):
        self.callback = callback
        return callback

    def getLinkedRECEvent(self):
        """If assigned by the user, get the RECEvent linked to this controller"""
        eventID = device.findEventID(self.getMIDIControlID())
        if eventID != midi.MaxInt:
            return RECEvent(eventID)

    def getMIDIControlID(self):
        return midi.EncodeRemoteControlID(self.port, self.channel, self.ccNumber)

    def matchesMsgEvent(self, event):
        status, channel = (event.status & 0xF0, event.status & 0x0F)
        return status == 0xB0 and event.data1 == self.ccNumber and channel == self.channel

    def OnControlChange(self, event):
        self.value_previous = self.value
        """Handler for FL events"""
        if self.matchesMsgEvent(event):
            self.updateValueFromEvent(event)
            if self.verbose:
                displayName = self.name or 'MidiControl({}, {})'.format(self.channel, hex(self.ccNumber))
                print('{} = {}'.format(displayName, self.value))
            if hasattr(self, "callback") and callable(self.callback):
                self.callback(self, event)

    def updateValueFromEvent(self, event):
        self.value = event.controlVal

    def sendFeedback(self, value):
        device.midiOutMsg((0xB0 + self.channel) + (self.ccNumber << 8) + (value << 16))

    # Available as a decorator!
    __call__ = set_callback

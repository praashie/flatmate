import midi
import device

from .event import RECEvent

DEFAULT_PORT = device.getPortNumber()

class MIDIControl:
    def __init__(self, channel, number, port=DEFAULT_PORT, name=''):
        self.channel = channel
        self.number = number
        self.port = port
        self.name = name
        self.value = 0
        self.value_previous = 0

        self.verbose = False
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback
        return callback

    def getLinkedRECEvent(self):
        """If assigned by the user, get the RECEvent linked to this controller"""
        midiControlID = midi.EncodeRemoteControlID(self.port, self.channel, self.number)
        eventID = device.findEventID(midiControlID)
        if eventID != midi.MaxInt:
            return RECEvent(eventID)

    def matchesMsgEvent(self, event):
        return event.controlNum == self.number and event.midiChan == self.channel

    def OnControlChange(self, event):
        self.value_previous = self.value
        """Handler for FL events"""
        if self.matchesMsgEvent(event):
            self.updateValueFromEvent(event)
            if self.verbose:
                displayName = self.name or 'MidiControl({}, {})'.format(self.channel, hex(self.number))
                print('{} = {}'.format(displayName, self.value))
            if callable(self.callback):
                self.callback(self, event)
                event.handled = True

    def updateValueFromEvent(self, event):
        self.value = event.controlVal

    def sendFeedback(self, value):
        device.midiOutMsg((0xB0 + self.channel) + (self.number << 8) + (value << 16))

    # Available as a decorator!
    __call__ = set_callback

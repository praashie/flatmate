# https://github.com/praashie/flatmate

import time

import midi
import channels
import mixer
import device

AUTOMATE_DEFAULT_FLAGS = midi.REC_Smoothed | midi.REC_UpdateValue | midi.REC_UpdateControl | midi.REC_SetChanged | midi.REC_FromMIDI

AUTOMATE_THROTTLING = False
AUTOMATE_THROTTLING_INTERVAL = 0.02

throttling_times = {}

def _automate(recid, *args):
    if AUTOMATE_THROTTLING:
        t = time.time()
        if (t - throttling_times.get(recid, 0)) < AUTOMATE_THROTTLING_INTERVAL:
            return
        throttling_times[recid] = t
    return mixer.automateEvent(recid, *args)

class RECEvent:
    """Wrapper for easily controlling FL Studio REC events.

    RECEvent implements __int__ and can be passed to FL's scripting API
    in place of its event ID integer."""

    def __init__(self, _id=0, default=0.0):
        self.id = _id
        self.value_default = 0.0

        self.last_automation_time = None

    def getName(self, shortName=False):
        """Get the name of the target control"""
        return mixer.getEventIDName(self.id, shortName)

    def getSplitName(self):
        return self.getName().partition(' - ')

    def getFloat(self, max=1.0, min=0.0):
        """Get the current value as a float between a range (default 0-1)"""
        return device.getLinkedValue(self.id)*(max-min) + min

    def getRaw(self):
        """Get the current value as a raw integer between 0-65536"""
        return mixer.getEventValue(self.id)

    def getMappedInt(self):
        """Get the current value in a different mapping called 'AutoSmooth'"""
        return mixer.getAutoSmoothEventValue(self.id)

    def getValueString(self):
        """Get the current value represented as a string"""
        return mixer.getEventIDValueString(self.id, self.getMappedInt())

    def getInfoFlags(self):
        return device.getLinkedInfo(self.id)

    def isCentered(self):
        """Return True if the target control is bipolar (panning etc.)"""
        return bool(self.getInfoFlags() & midi.Event_Centered)

    def setRaw(self, value, flags=AUTOMATE_DEFAULT_FLAGS):
        """Set the current value as a raw integer between 0-65536"""
        return _automate(self.id, value, flags)

    def setValue(self, value, max=1.0, min=0.0):
        """Set the current value as a float between a range (default 0-1)"""
        return self.setRaw(int(65536*(value-min)/(max-min)))

    def resetValue(self):
        self.setValue(self.value_default)

    def setIncrement(self, value, flags=AUTOMATE_DEFAULT_FLAGS, speed=0):
        """Increment the current value with a relative float between (0-1)"""
        return _automate(self.id, 1, flags, speed, 1, value)

    def touch(self):
        return _automate(self.id, 0, midi.REC_SetTouched)

    def __int__(self):
        return self.id

class MixerEvent(RECEvent):
    def __init__(self, track, n, default=0.0):
        self.track = track
        self.n = n
        self.value_default = default

    @property
    def id(self):
        return mixer.getTrackPluginId(self.track, 0) + self.n

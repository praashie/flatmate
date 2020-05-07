import midi
import channels
import mixer
import device

class RECEvent:
    def __init__(self, _id=0):
        self.id = _id

    def getName(self, shortName=False):
        return mixer.getEventIDName(self.id, shortName)

    def getFloat(self):
        return device.getLinkedValue(self.id)

    def getRaw(self):
        return mixer.getEventValue(self.id)

    def getMappedInt(self):
        return mixer.getAutoSmoothEventValue(self.id)

    def getValueString(self):
        return mixer.getEventIDValueString(self.id, self.getMappedInt())

    def getInfoFlags(self):
        return device.getLinkedInfo(self.id)

    def isCentered(self):
        return bool(self.getInfoFlags() & midi.Event_Centered)

    def setRaw(self, value, flags=midi.REC_MIDIController):
        return mixer.automateEvent(self.id, value, flags)

    def setValue(self, value, max=1.0, min=0.0):
        return self.setRaw(int(65536*(value-min)/(max-min)))

    def setIncrement(self, value, flags=midi.REC_MIDIController, speed=0):
        return mixer.automateEvent(self.id, 1, flags, speed, 1, value)

    def __int__(self):
        return self.id

class MixerEvent(RECEvent):
    def __init__(self, track, n):
        self.track = track
        self.n = n

    @property
    def id(self):
        return mixer.getTrackPluginId(self.track, 0) + midi.REC_Mixer_Send_Last + self.n

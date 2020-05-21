import midi
import mixer
from .event import RECEvent, MixerEvent

class PanEvent(MixerEvent):
    def getValueString(self):
        value = self.getFloat(min=-1.0, max=1.0)

        if value == 0.0:
            return "Cent."
        elif value == 1.0:
            return "Right"
        elif value == -1.0:
            return "Left"
        elif value > 0:
            return "{}% R".format(int(value*100))
        else:
            return "{}% L".format(int(-value*100))

class MixerTrack:
    def __init__(self, index):
        self.index = index

        self.volume = MixerEvent(index, midi.REC_Mixer_Vol)
        self.pan = PanEvent(index, midi.REC_Mixer_Pan)
        self.stereoSeparation = MixerEvent(index, midi.REC_Mixer_SS)

    def getName(self):
        return mixer.getTrackName(self.index)

    def setName(self, name):
        return mixer.setTrackName(self.index, name)

class MixerController:
    def __init__(self, track_width):
        self.track_width = track_width

        self.bank_start = 1

    def track(self, number):
        return MixerTrack(self.bank_start + number)

    def setBankStart(self, index):
        self.bank_start = index

    def bankUp(self):
        self.bank_start = min(127 - self.track_width, self.bank_start + self.track_width)

    def bankDown(self):
        self.bank_start = max(1, self.bank_start - self.track_width)

    def selectBank(self, focus=0):
        mixer.setTrackNumber(self.bank_start + focus, midi.curfxScrollToMakeVisible)
        for i in range(self.track_width):
            if i != focus:
                mixer.selectTrack(self.bank_start + i)

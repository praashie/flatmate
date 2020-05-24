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

        self.volume = MixerEvent(index, midi.REC_Mixer_Vol, default=0.8)
        self.pan = PanEvent(index, midi.REC_Mixer_Pan, default=0.5)
        self.stereoSeparation = MixerEvent(index, midi.REC_Mixer_SS, default=0.5)

    def getName(self):
        return mixer.getTrackName(self.index)

    def setName(self, name):
        return mixer.setTrackName(self.index, name)

    def mute(self, value=-1):
        mixer.muteTrack(self.index, value)

    def isMuted(self):
        return mixer.isTrackMuted(self.index)

    def solo(self, value=-1, flags=0):
        mixer.soloTrack(self.index, value, flags)

    def isSoloed(self):
        return mixer.isTrackSolo(self.index)

    def isSelected(self):
        return mixer.isTrackSelected(self.index)

    def select(self, value=True, single=True, flags=midi.curfxScrollToMakeVisible):
        if single and value:
            mixer.setTrackNumber(self.index, flags)
        elif value is None or bool(value) != bool(self.isSelected()):
            mixer.selectTrack(self.index)

    def getPeaks(self, mode=midi.PEAK_LR):
        return mixer.getTrackPeaks(self.index, mode)

class MixerController:
    def __init__(self, track_width):
        self.track_width = track_width
        self.bank_start = 1

        self.tracks = [MixerTrack(self.bank_start + i) for i in range(track_width)]

    def track(self, number):
        return self.tracks(number)

    def trackIndex(self, number):
        return self.bank_start + number

    def getAbsoluteTrackRange(self):
        return range(self.bank_start, self.bank_start + self.track_width)

    def setBankStart(self, index):
        self.bank_start = max(0, min(127 - self.track_width, index))

        for i, track in enumerate(self.tracks):
            track.index = self.trackIndex(i)

    def bankUp(self):
        self.setBankStart(self.bank_start + self.track_width)

    def bankDown(self):
        self.setBankStart(max(1, self.bank_start - self.track_width))

    def trackUp(self):
        self.setBankStart(self.bank_start + 1)

    def trackDown(self):
        self.setBankStart(self.bank_start - 1)

    def selectBank(self, focus=0):
        mixer.setTrackNumber(self.bank_start + focus, midi.curfxScrollToMakeVisible)
        for i in range(self.track_width):
            if i != focus:
                mixer.selectTrack(self.bank_start + i)

import device
import time

from .hooker import Hooker

def safe_getitem(container, index):
    if index < len(container):
        return container[index]
    return None

class MidiLCD:
    def __init__(self, sysex_prefix, width, height=1, character_map=None):
        self.sysex_prefix = sysex_prefix
        self.width = width
        self.height = height

        self.temp_message_duration = 2
        self.temp_message_time = None

        self.buffer = [("",)] * height

        Hooker.include(self)

    def write(self, text, row=0, temporary=False, align=''):
        if align:
            text = '{t:{a}{w}}'.format(t=text, a=align, w=self.width)

        text_bytes = text.encode("ascii", errors="ignore")
        device.midiOutSysex(self.sysex_prefix + text_bytes)

    def writeParts(self, text_parts, row=0, temporary=False, **kwargs):
        diff_parts = self.getBufferDifference(text_parts, row)
        if diff_parts is None:
            return

        if not temporary:
            self.buffer[row] = text_parts
        else:
            self.temp_message_time = time.time()

        text = ''.join(diff_parts)
        self.write(text, row=row, **kwargs)

    def clear(self):
        for i in range(self.height):
            self.buffer[i] = (" " * self.width,)
        self.redraw()

    def redraw(self):
        for i, line in enumerate(self.buffer):
            self.write(line, row=i)

    def OnIdle(self):
        if self.temp_message_time is not None:
            t = time.time()
            if (t - self.temp_message_time) >= self.temp_message_duration:
                self.temp_message_time = None
                self.redraw()

    def getBufferDifference(self, text_parts, row=0):
        differing_parts = None
        buffer_row = self.buffer[row]

        for i in range(max(len(text_parts), len(buffer_row))):
            part_buffer = safe_getitem(buffer_row, i)
            part_text = safe_getitem(text_parts, i)
            if part_buffer != part_text:
                if differing_parts is None:
                    differing_parts = (part_text,)
                else:
                    return text_parts # 2 or more differing parts

        return differing_parts


import device

from .hooker import Hooker
from .util import Timer

def safe_getitem(container, index):
    if index < len(container):
        return container[index]
    return None

class MidiLCD:
    def __init__(self, sysex_prefix, width, height=1, character_map=None, minInterval=None):
        self.sysex_prefix = sysex_prefix
        self.width = width
        self.height = height

        self.temp_message_timer = Timer(2)
        self.last_message_timer = Timer(minInterval)
        self.last_message_timer.start()

        self.pending_redraw = False

        self.buffer = [""] * height

        Hooker.include(self)

    def write(self, text, row=0, temporary=False, align=''):
        if not temporary:
            self.buffer[row] = text
        else:
            self.temp_message_timer.start()

        if self.last_message_timer.ready():
            self._write(text, row, align)
            self.last_message_timer.start()
        else:
            self.pending_redraw = True

    def _write(self, text, row=0, align=''):
        text = '{t:{a}{w}}'.format(t=text, a=align, w=self.width)
        self._send_bytes(text, row)

    def _send_bytes(self, text, row=0):
        text_bytes = text.encode("ascii", errors="ignore")
        device.midiOutSysex(self.sysex_prefix + text_bytes)
        self.pending_redraw = False

    def clear(self):
        for i in range(self.height):
            self.buffer[i] = (" " * self.width,)
        self.redraw()

    def redraw(self):
        for i, line in enumerate(self.buffer):
            self._write(line, row=i)

    def OnIdle(self):
        if self.temp_message_timer.ready():
            self.temp_message_timer.stop()
            self.pending_redraw = True
        if self.pending_redraw and self.last_message_timer.ready():
            self.redraw()
            self.last_message_timer.start()

    def isReady(self):
        return self.last_message_timer.ready()

class MidiLCDParts(MidiLCD):
    def __init__(self, *args, part_interval=1, **kwargs):
        self.part_refresh_timer = Timer(part_interval)
        self.part_refresh_timer.start()

        super().__init__(*args, **kwargs)
        self.final_buffer = ([("",)]) * self.height

    def getBufferDifference(self, text_parts, row=0):
        differing_parts = None
        buffer_row = self.final_buffer[row]

        for i in range(max(len(text_parts), len(buffer_row))):
            part_buffer = safe_getitem(buffer_row, i)
            part_text = safe_getitem(text_parts, i)
            if part_buffer != part_text:
                if differing_parts is None:
                    differing_parts = (part_text,)
                else:
                    return text_parts # 2 or more differing parts

        return differing_parts

    def _write(self, text_parts, row=0, temporary=False):
        diff_parts = self.getBufferDifference(text_parts, row)

        if diff_parts == text_parts:
            self.part_refresh_timer.start()
        elif self.part_refresh_timer.ready():
            if diff_parts is None:
                return
        else:
            diff_parts = text_parts

        self.final_buffer[row] = text_parts
        text = ''.join(diff_parts)
        self._send_bytes(text, row=row)

    def write(self, text, *args, **kwargs):
        text = (text,)
        super().write(text, *args, **kwargs)

    def writeParts(self, text_parts, *args, **kwargs):
        super().write(text_parts, *args, **kwargs)

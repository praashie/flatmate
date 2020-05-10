# https://github.com/praashie/flatmate

import device

def sendMessage(message_bytes):
    (status, byte1, byte2) = message_bytes

    device.midiOutMsg(status + (byte1 << 8) + (byte2 << 16))

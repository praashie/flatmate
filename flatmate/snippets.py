import device

def TranslateCC(cc_source, cc_target, clone=False):
    """Replace/clone a CC message with another CC number."""

    def OnControlChange(event):
        if event.controlNum == cc_source:
            if clone:
                device.ProcessMIDICC(event)
            event.controlNum = cc_target

            event.handled = True
    return OnControlChange

SustainFix = TranslateCC(0x40, 0x3F, clone=True)

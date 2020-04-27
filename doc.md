# Some details about the FL API

## channels

### getChannelIndex
`getChannelIndex(i: int) -> int`

Get the true channel index of the `i`th channel in currently shown group

## mixer

REC Events in general:
Internally stored as integers, (unconventional 0-65536, instead of 0-65535).

Each event also has an "AutoSmooth" mapping that represents this integer in another range. Usually this seems to be [0,16000]. For Mixer track panning, it's [-6400, 6400]. For channel rack panning, it's [0, 6400].

### getEventValue
`getEventValue(eventID: long, value: long = midi.MaxInt, smoothTarget: long = 1)`

If `value == midi.MaxInt`, get the current integer value for the given eventID (0-65536).

Otherwise, convert `value` from the `eventID`'s "AutoSmooth" mapping to the normal integer range.

### getAutoSmoothEventValue
`getAutoSmoothEventValue(eventID: long, locked: long = 1)`

Get the `eventID`'s current value in its "AutoSmooth" mapping range. No idea what `locked` does.

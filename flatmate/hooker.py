"""Manage entry points for FL Studio MIDI Scripts

Hooker makes it possible to merge multiple scripts together,
and hopefully encourages users to develop modular snippets.


Setup in a script module:
    from flatmate import Hooker

    Hooker.setVerbose()
    Hooker.install(globals())

"""

from .chain import Chain, EventChain

class HookerBase:
    def __init__(self, chains_dict):
        self.chains = chains_dict
        for name, chain in self.chains.items():
            chain.__name__ = name

    def setVerbose(self, verbose=True):
        """Enable/disable printing on function calls"""
        for c in self.chains.values():
            c.verbose = verbose

    def include(self, source, before=False):
        """Import and attach all compatible function chains from another object"""
        for function_name in self.chains:
            if hasattr(source, function_name):
                func = getattr(source, function_name)
                self.chains[function_name].attach(func, before=before)

    def install(self, namespace):
        """Install chains to a namespace (globals())

        Existing functions are wrapped automatically.

        """
        self._import_dict(namespace)
        namespace.update(self.chains)
        return namespace

    def _import_dict(self, source, before=False):
        for function_name in self.chains:
            if function_name in source:
                self.chains[function_name].attach(source[function_name], before=before)

    def __getattr__(self, attr):
        if attr in self.chains:
            return self.chains[attr]
        raise AttributeError

_chains = [
    'OnInit', 'OnDeInit', 'OnIdle', 'OnRefresh', 'OnDoFullRefresh',
    'OnUpdateBeatIndicator', 'OnDisplayZone', 'OnUpdateLiveMode',
    'OnDirtyMixerTrack', 'OnUpdateMeters', 'OnWaitingForInput', 'OnSendTempMsg']

_eventchains = ['OnMidiIn', 'OnMidiMsg', 'OnMidiOutMsg', 'OnNoteOn', 'OnNoteOff',
    'OnControlChange', 'OnProgramChange', 'OnPitchBend', 'OnKeyPressure',
    'OnChannelPressure']

_chain_dict = {}
for _c in _chains:
    _chain_dict[_c] = Chain()
for _c in _eventchains:
    _chain_dict[_c] = EventChain()


Hooker = HookerBase(_chain_dict)
Hooker.install(globals())

__all__ = _chains + _eventchains + ['Hooker']

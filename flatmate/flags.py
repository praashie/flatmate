# https://github.com/praashie/flatmate

import midi

FLAG_PREFIXES = ['PME', 'TLC', 'HW_Dirty', 'UF', 'GT']

class FlagParser:
    def __init__(self, prefix):
        self.__name__ = prefix
        self.flagtable = []
        for var in dir(midi):
            value = getattr(midi, var)
            if var.startswith(prefix + '_') and type(value) == int:
                self.flagtable.append(var)
                setattr(self, var[len(prefix)+1:], value)

    def __call__(self, x):
        return ' | '.join([flag for flag in self.flagtable if (x & getattr(midi, flag))])

def setup_tables(prefixes, namespace):
    for prefix in prefixes:
        namespace[prefix] = FlagParser(prefix)

setup_tables(FLAG_PREFIXES, globals())

GT.flagtable.remove("GT_All")
GT.flagtable.remove("GT_Cannot")

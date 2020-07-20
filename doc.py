# https://github.com/praashie/flatmate

"""Generate documentation of the FL Python environment"""

import sys
import _codecs as codecs

sys.path.append("Z:/usr/lib/python3.6/")

from encodings import utf_8

codecs.register(lambda encoding: utf_8.getregentry())

import _io as io

_f = None
def p(text):
    print(text)
    if _f:
        print(text, file=_f)

def indent_str(s, indent='    '):
    return '\n'.join([indent + line for line in s.splitlines()])

def write_module(module, modulename, write_path):
    global _f
    with io.open(write_path + '/' + modulename + '.txt', 'w', encoding="ascii") as f:
        _f = f
        p(handle_module(module, modulename))

    _f = None

def handle_module(module, name=None):
    if not name:
        name = module.__name__

    return handle_object(module, name="Module " + name)


def handle_object(x, name='<unnamed>'):
    s = name
    if x is None or type(x) in [int, str, float, bool]:
        s += " = " + repr(x) + "\n"
        return s
    if callable(x):
        s += "()"
    s += ":"

    if hasattr(x, '__doc__') and type(x.__doc__) == str:
        s += "\n" + indent_str(x.__doc__)
    s += "\n\n"

    for attrname in dir(x):
        if attrname.startswith("__"):
            continue
        s += indent_str(handle_object(getattr(x, attrname), name=attrname)) + "\n"

    return s

def run(path):
    targets = [(channelrack, 'local_channelrack'), (mixer, 'local_mixer')]

    for m in ['fl', 'screen', 'arrangement', 'gc', 'general', 'ui', 'mixer', 'patterns', 'playlist', 'transport', 'channels', 'device']:
        targets.append((__import__(m), m))

    for obj, name in targets:
        write_module(obj, name, path)


# https://github.com/praashie/flatmate
import math
import sys
from time import time

# Calculating a running average and variance:
# https://www.johndcook.com/blog/standard_deviation/

def format_timedelta(t):
    for prefix in (' ', 'm', 'μ', 'n'):
        if t >= 1.0:
            break
        t = t * 1000.0

    return '{:>5.1f} {}s'.format(t, prefix)

class Profiler:
    def __init__(self, name=''):
        self.name = name
        self.reset()

    def reset(self):
        self._running_mean = 0
        self._running_variance = 0
        self._sample_count = 0

        self.total = 0
        self.max = 0

        self._start_time = None

    def start(self):
        self._start_time = time()

    def stop(self):
        if self._start_time is None:
            return
        self._append(time() - self._start_time)
        self._start_time = None

    def mean(self):
        return self._running_mean

    def variance(self):
        if self._sample_count > 1:
            return self._running_variance / (self._sample_count - 1)
        return 0.0

    def sd(self):
        return math.sqrt(self.variance())

    def _append(self, x):
        self.total += x
        self.max = max(self.max, x)
        self._sample_count += 1
        if self._sample_count == 1:
            self._running_mean = x
        else:
            new_mean = self._running_mean + (x - self._running_mean) / self._sample_count
            self._running_variance += (x - self._running_mean) * (x - new_mean)
            self._running_mean = new_mean

    def __str__(self):
        return '{:<21}: max: {}, mean: {}, st.dev: {}, total: {}'.format(self.name,
            format_timedelta(self.max),
            format_timedelta(self.mean()),
            format_timedelta(self.sd()),
            format_timedelta(self.total))

class SysProfiler:
    def __init__(self):
        self.stats = {}

    def activate(self):
        sys.setprofile(self._profile)

    def deactivate(self):
        sys.setprofile(None)

    def _profile(self, frame, event, arg):
        fcode = frame.f_code
        fn = (fcode.co_filename, fcode.co_firstlineno, fcode.co_name)
        if not fn in self.stats:
            self.stats[fn] = Profiler(fcode.co_name)

        if event in ('call', 'c_call'):
            self.stats[fn].start()
        elif event in ('return', 'c_return'):
            self.stats[fn].stop()

    def print(self, sortkey="total"):
        frozen_stats = []
        for fn, profiler in self.stats.items():
            filename, lineno, fname = fn
            display_name = "{}:{}:{}".format(filename, lineno, fname)
            stat = {
                "name": display_name,
                "max": profiler.max,
                "mean": profiler.mean(),
                "sd": profiler.sd(),
                "total": profiler.total
            }
            frozen_stats.append(stat)

        frozen_stats.sort(key=lambda s: s[sortkey], reverse=True)

        fields = ("total", "max", "mean", "sd")

        print()
        print(("{:8} " * 5).format(*fields, "name"))
        for i, stat in zip(range(100), frozen_stats):
            line = " ".join([format_timedelta(stat[key]) for key in fields])
            line += " " + stat["name"]
            print(line)

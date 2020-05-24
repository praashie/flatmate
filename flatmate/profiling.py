# https://github.com/praashie/flatmate
from time import time

# Calculating a running average and variance:
# https://www.johndcook.com/blog/standard_deviation/

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
        return '{:<20}: max: {}, mean: {}, variance: {}, total: {}'.format(self.name,
            self.format_timedelta(self.max),
            self.format_timedelta(self.mean()),
            self.format_timedelta(self.variance()),
            self.format_timedelta(self.total))

    def format_timedelta(self, t):
        for prefix in ('', 'm', 'μ', 'n'):
            if t >= 1.0:
                break
            t = t * 1000.0

        return '{:.1f} {}s'.format(t, prefix)

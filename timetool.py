"""Time Clocker"""
import time as time

import warnings

from .utils import is_out_index
from .lib.BeautifyPrint import CSIcolor, _print

__all__ = ['Clocker']

class ClockAction():
    """Defined timer's clock time action."""
    def _time(self):
        return time.time()

    def _perf_counter(self):
        return time.perf_counter()

class Clocker(ClockAction):
    """record run time"""
    def __init__(self, action='time', putformat="{times}s") -> None:
        """`time` use time.time();
        `perf_counter` use time.perf_counter()"""
        super().__init__()
        self.unit = putformat

        clock_func = '_' + action
        if action not in ['time', 'perf_counter']:
            raise KeyError('Unknown action `%s`.'
                           ' Did you mean perf_counter/time?'
                            % action)

        self.__clock_time = getattr(self, clock_func)

        self.start()

    def start(self):
        """start clocker"""
        self.count = 0
        self.nonclock = True
        self.record_times = []
        self.start_time = self.__clock_time()

    def now(self):
        """output now runtime."""

        return self.runtime

    @property
    def clock(self):
        """Conduct a timekeeping and record it"""
        # TODO: 不超过100个记录，用固定长度列表
        if self.nonclock is True:
            self.nonclock = False
        self.count += 1
        self.record_times.append(self.runtime)
        return self

    @property
    def runtime(self):
        """return from start time to now run time"""
        return self.__clock_time()-self.start_time

    @property
    def avg_each(self):
        """Average time between two points"""
        return (self.record_times[-1])/(self.count)

    def put(self):
        """output time among last clock to start. 
        if not clock, it will output the runtime."""

        self.put_between(-1,-1)

    def put2(self):
        """output from last clock to previous stop"""
        if self.count < 2:
            self.put()
            return
        self.put_between(-2,-1)

    def put_between(self, start_point, end_point):
        """output times between start point and end point"""
        _s, _e = start_point, end_point
        if self.nonclock:
            times = self.runtime
        elif is_out_index([_s,_e],length=self.count):
            times = self.record_times[-1]
        elif _s == _e:
            times = self.record_times[_e]
        else:
            times = self.record_times[_e] - self.record_times[_s]
        self.__puts(times=times)

    def put_now_to_last_point(self):
        """output here to previous stop, `not record time of here`."""
        if self.count > 0:
            times = self.runtime-self.record_times[-1]
            self.__puts(times)
        else:
            warnings.warn(f"{CSIcolor.yellow}Not get clock.{CSIcolor.default}"
                        , Warning)

    def __puts(self, times):
        # output time
        _print(self.unit.format(times=times))

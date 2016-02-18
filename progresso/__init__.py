from datetime import datetime, timedelta
import shutil
import sys
import time


class Bar:

    prefix = 'Progress:'
    done_char = '='
    remain_char = ' '
    template = '\r{prefix} {progress} {percent:.1%} ({done}/{total})'
    done = 0
    start = None

    def __init__(self, total=None, **kwargs):
        self.columns = self.compute_columns()
        self.total = total
        self.__dict__.update(kwargs)
        if not self.template.startswith('\r'):
            self.template = '\r' + self.template

    def compute_columns(self):
        return shutil.get_terminal_size((80, 20)).columns

    def keys(self):
        return [k for k in dir(self)
                if not k.startswith('_') and not k == "progress"]

    def __getitem__(self, item):
        return getattr(self, item, '')

    @property
    def progress(self):
        done_chars = int(self.fraction * self.length)
        remain_chars = self.length - done_chars
        return self.done_char * done_chars + self.remain_char * remain_chars

    @property
    def percent(self):
        return self.fraction

    @property
    def lasting(self):
        return timedelta(seconds=self.remaining_time)

    @property
    def elapsed(self):
        return timedelta(seconds=self.raw_elapsed, microseconds=0)

    @property
    def eta(self):
        return datetime.now() + self.lasting

    @property
    def avg(self):
        return round(self.raw_avg, 1)

    def _update(self):
        self.remaining = self.total - self.done
        self.fraction = min(self.done / self.total, 1.0)
        self.raw_elapsed = time.time() - self.start
        self.raw_avg = self.raw_elapsed / self.done
        self.remaining_time = self.remaining * self.raw_avg

        line = self.template.format(progress='{}', **self)

        self.length = self.columns - len(line) - 2

        sys.stdout.write(line.format(self.progress))

        if self.fraction == 1.0:
            sys.stdout.write('\n')

        sys.stdout.flush()

    def __call__(self, **kwargs):
        self.update(**kwargs)

    def update(self, step=1, done=None):
        if self.start is None:
            self.start = time.time()
        if done is not None:
            self.done = done
        else:
            self.done += step

        self._update()

    def __next__(self):
        self.update()

    def iter(self, iterable):
        for i in iterable:
            self.update()
            yield i

from datetime import datetime, timedelta
import re
import shutil
import sys
import time

VARS = re.compile('\{(.*?)\}')


class Bar:

    prefix = 'Progress:'
    done_char = '='
    remain_char = ' '

    def __init__(self, total=None, **kwargs):
        self.columns = self.compute_columns()
        self.total = total
        self.template = '\r{prefix} {progress} {percent} ({done}/{total})'
        self.done = 0
        self.start = None
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.widgets = VARS.findall(self.template)
        self.widgets.remove('progress')
        if not self.template.startswith('\r'):
            self.template = '\r' + self.template

    def compute_columns(self):
        return shutil.get_terminal_size((80, 20)).columns

    @property
    def progress(self):
        done_chars = int(self.fraction * self.length)
        remain_chars = self.length - done_chars
        return self.done_char * done_chars + self.remain_char * remain_chars

    @property
    def percent(self):
        return '{}%'.format(str(int(self.fraction * 1000) / 10))

    @property
    def lasting(self):
        return timedelta(seconds=self.remaining_time)

    @property
    def elapsed(self):
        return timedelta(seconds=self.raw_elapsed, microseconds=0)

    @property
    def eta(self):
        d = datetime.now() + self.lasting
        tpl = '{:%H:%M:%S}'
        if self.lasting.days:
            tpl = '{:%Y-%m-%d %H:%M:%S}'
        return tpl.format(d)

    @property
    def avg(self):
        return round(self.raw_avg, 1)

    def _update(self):
        self.remaining = self.total - self.done
        self.fraction = min(self.done / self.total, 1.0)
        self.raw_elapsed = time.time() - self.start
        self.raw_avg = self.raw_elapsed / self.done
        self.remaining_time = self.remaining * self.raw_avg

        data = {name: getattr(self, name) for name in self.widgets}
        line = self.template.format(progress='{}', **data)

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

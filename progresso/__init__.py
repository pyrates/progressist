from datetime import datetime, timedelta
import shutil
import sys
import time


class Bar:

    prefix = 'Progress:'
    done_char = '='
    remain_char = ' '
    template = '{prefix} {progress} {percent} ({done}/{total})'
    done = 0
    total = 0
    start = None
    steps = ('-', '\\', '|', '/')
    progress = '{bar}'
    invisible_chars = 1  # "\r"

    def __init__(self, **kwargs):
        self.columns = self.compute_columns()
        self.__dict__.update(kwargs)
        if not self.template.startswith('\r'):
            self.template = '\r' + self.template

    def compute_columns(self):
        return shutil.get_terminal_size((80, 20)).columns

    def keys(self):
        return [k for k in dir(self) if not k.startswith('_')]

    def __getitem__(self, item):
        return getattr(self, item, '')

    @property
    def spinner(self):
        step = self.done % len(self.steps)
        return self.steps[int(step)]

    @property
    def bar(self):
        done_chars = int(self.fraction * self.free_space)
        remain_chars = self.free_space - done_chars
        return self.done_char * done_chars + self.remain_char * remain_chars

    @property
    def percent(self):
        return Percent(self.fraction)

    @property
    def tta(self):
        """Time to arrival."""
        return timedelta(seconds=self.remaining_time)

    @property
    def elapsed(self):
        """Elasped time from the start."""
        return timedelta(seconds=self.raw_elapsed, microseconds=0)

    @property
    def eta(self):
        """Estimated time of arrival."""
        return ETA.from_datetime(datetime.now() + self.tta)

    @property
    def avg(self):
        """Average iterations by second."""
        return round(self.raw_avg, 1)

    def render(self):
        self.remaining = self.total - self.done
        self.fraction = min(self.done / self.total, 1.0) if self.total else 0
        self.raw_elapsed = time.time() - self.start
        self.raw_avg = self.raw_elapsed / self.done if self.done else 0
        self.remaining_time = self.remaining * self.raw_avg

        # format_map(self) instead of format(**self) to prevent all properties
        # to be evaluated, even ones not needed for the given template.
        line = self.template.format_map(self)

        self.free_space = (self.columns - len(line) + len(self.progress)
                           + self.invisible_chars)
        sys.stdout.write(line.format_map(self))

        if self.fraction == 1.0:
            self.finish()
        else:
            sys.stdout.flush()

    def finish(self):
        sys.stdout.write('\n')

    def __call__(self, **kwargs):
        self.update(**kwargs)

    def update(self, step=1, **kwargs):
        if self.start is None:
            self.start = time.time()
        if step:
            self.done += step
        # Allow to override any properties.
        self.__dict__.update(kwargs)

        self.render()

    def __next__(self):
        self.update()

    def iter(self, iterable):
        for i in iterable:
            yield i
            self.update()
        if self.fraction != 1.0:
            # Spinner without total.
            self.finish()


# Manage sane default formats while keeping the original type to allow any
# built-in formatting syntax.

class Percent(float):

    def __format__(self, format_spec):
        if not format_spec:
            format_spec = '.2%'
        return super().__format__(format_spec)


class ETA(datetime):

    def __format__(self, format_spec):
        if not format_spec:
            now = datetime.now()
            diff = self - now
            format_spec = '%H:%M:%S'
            if diff.days > 1:
                format_spec = '%Y-%m-%d %H:%M:%S'
        return super().__format__(format_spec)

    @classmethod
    def from_datetime(cls, dt):
        # Find a more elegant way.
        return cls(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour,
                   minute=dt.minute, second=dt.second, tzinfo=dt.tzinfo)

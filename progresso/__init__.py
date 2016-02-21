from datetime import datetime, timedelta
import shutil
import string
import sys
import time


class Formatter(string.Formatter):
    """
    Allow to have some custom formatting types.
    """

    def format_bytes(self, size, spec=None):
        SUFFIXES = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
        spec = spec or '.1'
        for suffix in SUFFIXES:
            size /= 1024
            if size < 1024:
                return '{value:{spec}f} {suffix}'.format(value=size, spec=spec,
                                                         suffix=suffix)

    def format_field(self, value, format_string):
        if format_string.endswith("B"):
            spec = format_string[:-1]
            return self.format_bytes(int(value), spec=spec)
        else:
            return super().format_field(value, format_string)


class Bar:

    prefix = 'Progress:'
    done_char = '='
    remain_char = ' '
    template = '{prefix} {animation} {percent} ({done}/{total})'
    done = 0
    total = 0
    start = None
    steps = ('-', '\\', '|', '/')
    animation = '{progress}'
    invisible_chars = 1  # "\r"
    supply = 0

    def __init__(self, **kwargs):
        self.columns = self.compute_columns()
        self.__dict__.update(kwargs)
        if not self.template.startswith('\r'):
            self.template = '\r' + self.template
        self.formatter = Formatter()

    def format(self, tpl, *args, **kwargs):
        return self.formatter.vformat(tpl, None, self)

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
    def progress(self):
        if not self.free_space:
            return ''
        done_chars = int(self.fraction * self.free_space)
        remain_chars = self.free_space - done_chars
        return self.done_char * done_chars + self.remain_char * remain_chars

    @property
    def stream(self):
        chars = []
        for i in range(self.free_space):
            idx = (self.done + i) % len(self.steps)
            chars.append(self.steps[idx])
        return ''.join(chars)

    @property
    def percent(self):
        return Percent(self.fraction)

    @property
    def tta(self):
        """Time to arrival."""
        return Timedelta(seconds=self.remaining_time)

    @property
    def elapsed(self):
        """Elasped time from the start."""
        return Timedelta(seconds=self.raw_elapsed)

    @property
    def eta(self):
        """Estimated time of arrival."""
        return ETA.from_datetime(datetime.now() + self.tta)

    @property
    def speed(self):
        """Number of iterations per second."""
        return Float(1.0 / self.avg if self.avg else 0)

    def render(self):
        if self.start is None:
            self.start = time.time()
        self.free_space = 0
        self.remaining = self.total - self.done
        self.addition = self.done - self.supply
        self.fraction = min(self.done / self.total, 1.0) if self.total else 0
        self.raw_elapsed = time.time() - self.start
        self.avg = Float(self.raw_elapsed / self.addition if self.addition else 0)
        self.remaining_time = self.remaining * self.avg

        # format_map(self) instead of format(**self) to prevent all properties
        # to be evaluated, even ones not needed for the given template.
        line = self.format(self.template)

        self.free_space = (self.columns - len(line) + len(self.animation)
                           + self.invisible_chars)
        sys.stdout.write(self.format(line))

        if self.fraction >= 1.0:
            self.finish()
        else:
            sys.stdout.flush()

    def finish(self):
        sys.stdout.write('\n')

    def __call__(self, **kwargs):
        self.update(**kwargs)

    def update(self, step=1, **kwargs):
        if step:
            self.done += step
        # Allow to override any properties.
        self.__dict__.update(kwargs)
        if self.start is None and 'done' in kwargs:
            # First call to update and forcing a done value. May be
            # resuming a download. Keep track for better ETA computation.
            self.supply = self.done
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

class Float(float):

    def __format__(self, format_spec):
        if not format_spec:
            format_spec = '.2f'
        return super().__format__(format_spec)


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


class Timedelta(timedelta):

    def __new__(cls, **kwargs):
        tmp = timedelta(**kwargs)
        # Filter out microseconds from str format.
        # timedelta does not have a __format__ method, and we don't want to
        # recode it (we would need to handle i18n of "days").
        obj = timedelta(days=tmp.days, seconds=tmp.seconds)
        return obj


VERSION = (0, 0, 1)

__author__ = 'Yohan Boniface'
__contact__ = "hi@yohanboniface.me"
__homepage__ = "https://github.com/yohanboniface/progresso"
__version__ = ".".join(map(str, VERSION))

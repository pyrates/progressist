import datetime
import shutil
import string
import sys
import time

try:
    import pkg_resources
except ImportError:  # pragma: no cover
    pass
else:
    if __package__:
        VERSION = pkg_resources.get_distribution(__package__).version


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

    def format_int(self, value):
        # Force integer representation.
        try:
            value = int(value)
        except ValueError:
            pass
        return str(value)

    def format_field(self, value, format_string):
        if format_string.endswith("B"):
            spec = format_string[:-1]
            return self.format_bytes(int(value), spec=spec)
        elif format_string.endswith("D"):
            return self.format_int(value)
        return super().format_field(value, format_string)


class ProgressBar:

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
    outro = '\n'
    throttle = 0  # Do not render unless done step is more than throttle.
    fraction = 0
    prints = 0

    def __init__(self, **kwargs):
        self.columns = self.compute_columns()
        self.__dict__.update(kwargs)
        if not self.template.startswith('\r'):
            self.template = '\r' + self.template
        self.formatter = Formatter()
        self._last_render = 0
        if self.throttle:
            if not isinstance(self.throttle, (int, float, datetime.timedelta)):
                raise ValueError('Invalid type for throttle: '
                                 '{}'.format(type(self.throttle)))
            if isinstance(self.throttle, float) and self.throttle > 1.0:
                raise ValueError('Float throttle must be between 0 and 1.0. '
                                 'Got {} instead.'.format(self.throttle))

    def format(self, tpl, *args, **kwargs):
        return self.formatter.vformat(tpl, None, self)

    def compute_columns(self):
        return shutil.get_terminal_size((80, 20)).columns

    def __getitem__(self, item):
        return getattr(self, item, '')

    @property
    def spinner(self):
        step = self.prints % len(self.steps)
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
            idx = (self.prints + i) % len(self.steps)
            chars.append(self.steps[idx])
        return ''.join(chars)

    @property
    def percent(self):
        return Percent(self.fraction)

    @property
    def eta(self):
        """Estimated time of arrival."""
        remaining_time = datetime.timedelta(seconds=self.tta)
        return ETA(datetime.datetime.now() + remaining_time)

    @property
    def speed(self):
        """Number of iterations per second."""
        return Float(1.0 / self.avg if self.avg else 0)

    @property
    def throttled(self):
        if not self.throttle:
            return False
        if isinstance(self.throttle, (int, float)):
            throttle = self.throttle
            if isinstance(self.throttle, float):
                throttle = max(1, self.total * self.throttle)
            throttle = self._last_render + throttle
            if self.done < throttle:
                if (not self.total or throttle <= self.total
                   or self.done < self.total):
                    return True
            self._last_render = self.done
        elif isinstance(self.throttle, datetime.timedelta):
            if ((not self.total or self.done < self.total) and
               self._last_render + self.throttle.seconds > time.time()):
                return True
            self._last_render = time.time()
        return False

    def render(self):
        if self.throttled:
            return
        if self.start is None:
            self.start = time.time()
        self.free_space = 0
        self.remaining = self.total - self.done
        self.addition = self.done - self.supply
        self.fraction = min(self.done / self.total, 1.0) if self.total else 0
        self.elapsed = Timedelta(time.time() - self.start)
        self.avg = Float(self.elapsed / self.addition if self.addition else 0)
        self.tta = Timedelta(self.remaining * self.avg)

        line = self.format(self.template)

        self.free_space = (self.columns - len(line) + len(self.animation)
                           + self.invisible_chars)
        sys.stdout.write(self.format(line))
        self.prints += 1

        if self.fraction >= 1.0:
            self.finish()
        else:
            sys.stdout.flush()

    def finish(self):
        if not self.total and self.throttle:
            # In "no total" mode, we cannot know that we are doing the last
            # iteration to force rendering, so let's force render on finish.
            self.throttle = False
            self.render()
        sys.stdout.write(self.format(self.outro))

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

    def on_urlretrieve(self, blocknum, bs, size):
        """Callback to use with urllib.request.urlretrieve"""
        done = blocknum * bs
        total = size if size > -1 else 0
        if total:
            # We don't have the real amount of bytes read, but the theorical
            # amount, so on the last chunk the real amount may be smaller.
            done = min(done, total)
        self.update(done=done, total=total)


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


class ETA(datetime.datetime):

    def __new__(cls, *args, **kwargs):
        if args and not isinstance(args[0], int):
            # datetime + timedelta returns a datetime, while we want an ETA.
            dt = args[0]
            return super().__new__(cls, year=dt.year, month=dt.month,
                                   day=dt.day, hour=dt.hour, minute=dt.minute,
                                   second=dt.second, tzinfo=dt.tzinfo)
        else:
            return super().__new__(cls, *args, **kwargs)

    def __format__(self, format_spec):
        if not format_spec:
            now = datetime.datetime.now()
            diff = self - now
            format_spec = '%H:%M:%S'
            if diff.days > 0:
                format_spec = '%Y-%m-%d %H:%M:%S'
        return super().__format__(format_spec)


class Timedelta(int):
    """An integer that is formatted by default as timedelta."""

    def format_as_timedelta(self):
        """Format seconds as timedelta."""
        # Do we want this as a Formatter type also?
        tmp = datetime.timedelta(seconds=self)
        # Filter out microseconds from str format.
        # timedelta does not have a __format__ method, and we don't want to
        # recode it (we would need to handle i18n of "days").
        obj = datetime.timedelta(days=tmp.days, seconds=tmp.seconds)
        return str(obj)

    def __format__(self, format_spec):
        if not format_spec:
            return self.format_as_timedelta()
        return super().__format__(format_spec)

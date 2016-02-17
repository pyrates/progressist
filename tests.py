import time

try:
    import psutil
except ImportError:
    psutil = None
from progresso import Bar


def loop():
    for i in range(20):
        time.sleep(0.2)
        yield True


def call(bar):
    for x in bar.iter(loop()):
        continue


def test_default():
    """Default bar."""
    bar = Bar(total=20)
    call(bar)


def test_custom_done_char():
    """Custom fill character."""
    bar = Bar(total=20, done_char='█')
    call(bar)


def test_custom_remain_char():
    """Custom empty fill character."""
    bar = Bar(total=20, done_char='◉', remain_char='◯')
    call(bar)


def test_with_eta():
    """Display ETA."""
    bar = Bar(total=20, template='{prefix} {progress} {eta}')
    call(bar)


def test_with_avg():
    """Display avg."""
    bar = Bar(total=20, template='{prefix} {progress} Avg: {avg} loop/s')
    call(bar)


def test_with_custom_color():
    """Custom color."""
    bar = Bar(total=20,
              template="\r\033[34m{prefix} {progress} {percent}\033[39m")
    call(bar)


def test_with_custom_class():
    """Using a custom class with custom method to get current swap"""

    class MyBar(Bar):

        @property
        def swap(self):
            if not psutil:
                return "psutil not installed"
            return psutil.swap_memory().total

    bar = MyBar(total=20, template='{prefix} {progress} Swap: {swap}')
    call(bar)


def test_spinner():
    """Using a custom class to create a spinner"""

    class MyBar(Bar):
        steps = ('-', '\\', '|', '/')

        @property
        def progress(self):
            step = self.done % len(self.steps)
            return self.steps[step]

    bar = MyBar(total=20)
    call(bar)


if __name__ == '__main__':

    for name, func in globals().copy().items():
        if name.startswith('test_'):
            print(func.__doc__)
            func()

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
    bar = Bar(total=20, prefix="Default:")
    call(bar)


def test_custom_done_char():
    bar = Bar(total=20, done_char='█', prefix="Custom fill character:")
    call(bar)


def test_custom_remain_char():
    """Custom empty fill character."""
    bar = Bar(total=20, done_char='◉', remain_char='◯',
              prefix="Custom empty fill char:")
    call(bar)


def test_with_eta():
    bar = Bar(total=20, template='With ETA: {progress} ETA: {eta}')
    call(bar)


def test_with_avg():
    bar = Bar(total=20, template='With Average: {progress} Avg: {avg} loop/s')
    call(bar)


def test_with_custom_color():
    bar = Bar(total=20,
              template="\r\033[34mCustom color: {progress} {percent}\033[39m")
    call(bar)


def test_with_custom_class():

    class MyBar(Bar):

        @property
        def swap(self):
            if not psutil:
                return "psutil not installed"
            return psutil.swap_memory().total

    bar = MyBar(total=20,
                template='Custom class with custom info: '
                         '{progress} Swap: {swap}')
    call(bar)


def test_spinner():

    class MyBar(Bar):
        steps = ('-', '\\', '|', '/')

        @property
        def progress(self):
            step = self.done % len(self.steps)
            return self.steps[step]

    bar = MyBar(total=20, prefix="Custom class with spinner")
    call(bar)


if __name__ == '__main__':

    for name, func in globals().copy().items():
        if name.startswith('test_'):
            func()

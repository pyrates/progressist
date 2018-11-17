from datetime import timedelta
import sys
import time

try:
    import psutil
except ImportError:
    psutil = None
from progressist import ProgressBar


def loop():
    for i in range(20):
        time.sleep(0.2)
        yield True


def call(bar):
    for x in bar.iter(loop()):
        continue


REGISTRY = []


def register(func):
    REGISTRY.append(func)
    return func


@register
def example_default():
    bar = ProgressBar(total=20, prefix="Default:")
    call(bar)


@register
def example_custom_done_char():
    bar = ProgressBar(total=20, done_char='█', prefix="Custom fill character:")
    call(bar)


@register
def example_custom_remain_char():
    """Custom empty fill character."""
    bar = ProgressBar(total=20, done_char='◉', remain_char='◯',
                      prefix="Custom empty fill char:")
    call(bar)


@register
def example_with_eta():
    bar = ProgressBar(total=20, template='With ETA: {animation} ETA: {eta}')
    call(bar)


@register
def example_with_avg():
    bar = ProgressBar(total=20,
                      template='With Average: {animation} Avg: {avg} s/item')
    call(bar)


@register
def example_with_custom_color():
    bar = ProgressBar(total=20, remain_char='-', invisible_chars=11,
                      template="\r\033[34mCustom color: {animation}\033[39m")
    call(bar)


@register
def example_with_custom_class():

    class MyBar(ProgressBar):

        @property
        def swap(self):
            if not psutil:
                return "psutil not installed"
            return psutil.swap_memory().total

    bar = MyBar(total=20,
                template='Custom class with custom info: '
                         '{animation} Swap: {swap}')
    call(bar)


@register
def example_stream():

    bar = ProgressBar(total=20, animation='{stream}', steps=['⎻', '⎼'],
                      template='Stream {animation} {elapsed}')
    call(bar)


@register
def example_throttle():

    bar = ProgressBar(total=20, throttle=2, prefix='Throttling')
    call(bar)


@register
def example_throttle_by_second():

    bar = ProgressBar(total=20, throttle=timedelta(seconds=1),
                      prefix='Throttling by second')
    call(bar)


@register
def example_spinner():

    bar = ProgressBar(total=20, prefix="Spinner", animation='{spinner}')
    call(bar)


@register
def example_spinner_without_total():

    bar = ProgressBar(animation='{spinner}',
                      steps=['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'],
                      template='Spinner without total: {animation} '
                               'Elapsed: {elapsed}')
    call(bar)


@register
def example_reverse_bar():

    class MyBar(ProgressBar):

        @property
        def progress(self):
            done_chars = int(self.fraction * self.free_space)
            remain_chars = self.free_space - done_chars
            return (self.remain_char * remain_chars
                    + self.done_char * done_chars)

    bar = MyBar(total=20, template="{percent} {animation} Reverse bar")
    call(bar)


@register
def example_download():

    class DownloadBar(ProgressBar):
        """Example of a resuming download, displaying human readable sizes."""
        template = ('Download |{animation}| {done:B}/{total:B} ({speed:B}/s)')
        done_char = '█'

    bar = DownloadBar()
    for i in range(82944500, 197739688 + 165889, 165889):
        time.sleep(0.002)
        bar.update(done=i, total=197739688)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        for func in REGISTRY:
            if func.__name__ == sys.argv[1]:
                func()
                break
        else:
            print('No func found with name', sys.argv[1])
    else:
        for func in REGISTRY:
            func()

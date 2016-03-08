import time
import datetime

import pytest


@pytest.mark.parametrize('input,expected', [
    (12, '0.0 KiB'),
    (1098, '1.1 KiB'),
    (109830983, '104.7 MiB'),
    (109830983809823, '99.9 TiB'),
])
def test_format_bytes(input, expected):
    from progressist import Formatter
    fmt = Formatter()
    assert fmt.format('{:B}', input) == expected


@pytest.mark.parametrize('input,expected', [
    (12, '12'),
    ('12', '12'),
    (12.0, '12'),
    ('notcastable', 'notcastable'),
])
def test_format_int(input, expected):
    from progressist import Formatter
    fmt = Formatter()
    assert fmt.format('{:D}', input) == expected


def test_default(bar, capsys):
    bar.update(done=37)
    out, err = capsys.readouterr()
    assert out == '\rBar: ==============                         37/100'
    bar.update(done=50)
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                    50/100'
    bar.update(done=86)
    out, err = capsys.readouterr()
    assert out == '\rBar: ================================       86/100'


def test_update_by_one_step(bar, capsys):
    bar.done = 49
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ==================                     49/100'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                    50/100'


def test_update_by_more_than_one_step(bar, capsys):
    bar.done = 50
    bar.update(step=7)
    out, err = capsys.readouterr()
    assert out == '\rBar: =====================                  57/100'


def test_iter(bar, capsys):
    for i in bar.iter(range(100)):
        out, err = capsys.readouterr()
        if i == 50:
            assert out == '\rBar: ===================                    50/100'  # noqa


def test_custom_done_char(bar, capsys):
    bar.done_char = '#'
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ###################                    50/100'


def test_custom_remain_char(bar, capsys):
    bar.remain_char = '-'
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================------------------- 50/100'


def test_percent(bar, capsys):
    bar.template = '\r{prefix} {animation} {percent}'
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                    50.00%'
    bar.done = 78.2134
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: =============================          78.21%'


def test_can_override_percent_formatting(bar, capsys):
    bar.template = '\r{prefix} {animation} {percent:.1%}'
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                     50.0%'
    bar.done = 78.2134
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ==============================          78.2%'


def test_avg(bar, capsys):
    bar.template = '\r{prefix} {animation} {avg}/s'
    bar.start = time.time() - 25
    bar.done = 43
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ================                       0.58/s'
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                    0.50/s'


def test_can_override_avg_formatting(bar, capsys):
    bar.template = '\r{prefix} {animation} {avg:.1f}/s'
    bar.start = time.time() - 25
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                     0.5/s'


def test_speed(bar, capsys):
    bar.template = '\r{prefix} {animation} {speed} loop/s'
    bar.start = time.time() - 25
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ================                  2.00 loop/s'
    bar.done = 89
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: =============================     3.56 loop/s'


def test_can_override_speed_formatting(bar, capsys):
    bar.template = '\r{prefix} {animation} {speed:.1f} loop/s'
    bar.start = time.time() - 25
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: =================                  2.0 loop/s'


def test_spinner(bar, capsys):
    bar.animation = '{spinner}'
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: - 0/100'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rBar: \\ 1/100'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rBar: | 2/100'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rBar: / 3/100'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rBar: - 4/100'


def test_spinner_without_total(bar, capsys):
    bar.total = 0
    bar.animation = '{spinner}'
    bar.template = '\rSpinner: {animation}'
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rSpinner: -'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rSpinner: \\'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rSpinner: |'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rSpinner: /'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rSpinner: -'


def test_custom_spinner_steps(bar, capsys):
    bar.steps = ['#', '*']
    bar.animation = '{spinner}'
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: # 0/100'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rBar: * 1/100'


def test_throttle(bar, capsys):
    bar.throttle = 5
    bar.update(done=37)
    out, err = capsys.readouterr()
    assert out == '\rBar: ==============                         37/100'
    bar.update(done=38)
    out, err = capsys.readouterr()
    assert out == ''
    bar.update(done=42)
    out, err = capsys.readouterr()
    assert out == '\rBar: ===============                        42/100'
    bar.update(done=99)
    out, err = capsys.readouterr()
    assert out == '\rBar: =====================================  99/100'
    bar.update(done=100)
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================================== 100/100\n'


def test_eta(bar, capsys, monkeypatch):

    class fake_datetime(datetime.datetime):
        @classmethod
        def now(cls):
            return datetime.datetime(2016, 4, 7, 1, 2, 3)

    def fake_time():
        return datetime.datetime.now().timestamp()

    monkeypatch.setattr(datetime, 'datetime', fake_datetime)
    monkeypatch.setattr(time, 'time', fake_time)
    # 3 seconds for doing 50% for the job.
    bar.start = datetime.datetime.now().timestamp() - 3
    bar.template = '\r{prefix} {animation} {eta}'
    bar.update(done=50)
    out, err = capsys.readouterr()
    assert out == '\rBar: ==================                   01:02:06'


def test_more_than_24_hours_eta(bar, capsys, monkeypatch):

    class fake_datetime(datetime.datetime):
        @classmethod
        def now(cls):
            return datetime.datetime(2016, 4, 7, 1, 2, 3)

    def fake_time():
        return datetime.datetime.now().timestamp()

    monkeypatch.setattr(datetime, 'datetime', fake_datetime)
    monkeypatch.setattr(time, 'time', fake_time)
    # 1 day and 1 second for doing 50% for the job.
    bar.start = datetime.datetime.now().timestamp() - (60 * 60 * 24 + 1)
    bar.template = '\r{prefix} {animation} {eta}'
    bar.update(done=50)
    out, err = capsys.readouterr()
    assert out == '\rBar: ============              2016-04-08 01:02:04'


def test_tta(bar, capsys, monkeypatch):

    bar.start = datetime.datetime.now().timestamp() - 3
    bar.template = '\r{prefix} {animation} {tta}'
    bar.update(done=50)
    out, err = capsys.readouterr()
    assert out == '\rBar: ==================                    0:00:03'


def test_tta_can_be_formatted_as_int(bar, capsys, monkeypatch):

    bar.start = datetime.datetime.now().timestamp() - 3
    bar.template = '\r{prefix} {animation} | Remaining: {tta:d} seconds'
    bar.update(done=50)
    out, err = capsys.readouterr()
    assert out == '\rBar: ===========            | Remaining: 3 seconds'


def test_stream(bar, capsys):
    bar.animation = '{stream}'
    bar.steps = ['⎻', '⎼']
    bar.update(50)
    out, err = capsys.readouterr()
    assert out == '\rBar: ⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼⎻⎼ 50/100'


def test_call(bar, capsys):
    bar(done=37)
    out, err = capsys.readouterr()
    assert out == '\rBar: ==============                         37/100'
    bar(done=50)
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                    50/100'
    bar(done=86)
    out, err = capsys.readouterr()
    assert out == '\rBar: ================================       86/100'


def test_next(bar, capsys):
    bar.done = 37
    next(bar)
    out, err = capsys.readouterr()
    assert out == '\rBar: ==============                         38/100'

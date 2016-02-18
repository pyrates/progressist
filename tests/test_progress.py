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
    bar.template = '\r{prefix} {progress} {percent}'
    bar.done = 50
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: ===================                    50.00%'
    bar.done = 78.2134
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: =============================          78.21%'


def test_spinner(bar, capsys):
    bar.progress = '{spinner}'
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
    bar.progress = '{spinner}'
    bar.template = '\rSpinner: {progress}'
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
    bar.progress = '{spinner}'
    bar.render()
    out, err = capsys.readouterr()
    assert out == '\rBar: # 0/100'
    bar.update()
    out, err = capsys.readouterr()
    assert out == '\rBar: * 1/100'

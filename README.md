# Progresso

Minimalist and pythonic progress bar.


## Install

    pip install git+https://github.com/yohanboniface/progresso  # No pypi package yet


## Usage

    from progresso import Bar
    bar = Bar(total=mytotalstuff)
    for item in mystuff:
        do_stuff
        bar.update()

Or use `bar.iter` transparently

    for item in bar.iter(mystuff):
        do_stuff

You can step by more than one at a time:

    for item in mystuff:
        amount = do_stuff()
        bar.update(step=amount)

You can change the fill character:

    bar = Bar(total=mytotalstuff, done_char='#')

You can change the whole template:

    bar = Bar(total=mytotalstuff, template='{prefix} {progress} ETA: {eta}')

It's just plain [python formatting](https://docs.python.org/3.4/library/string.html#formatspec)
so you can use any valid string formatting to take control over the appearance.
For example:

    bar = Bar(total=mytotalstuff, template='{progress} {percent:.2%} ETA: {eta:%H:%M:%S}')

You can change the progress logic itself, for example to use a spinner (included):

    bar = Bar(total=mytotalstuff, progress='{spinner}')
    # 'progress' kwarg must return a valid template variable.
    # included ones are {bar} and {spinner}

You can add more widgets by subclassing it:

    class MyBar(Bar):

        @property
        def swap(self):
            return psutil.swap_memory().total

    bar = MyBar(total=20, template='{prefix} {progress} Swap usage: {swap}')

See [tests](https://github.com/yohanboniface/progresso/blob/poc/tests.py) for more
examples.


## Parameters

| name  | default | description |
| ----- | ------ | ------------- |
| done_char | `=` | Char used for filling the progress bar |
| remain_char | `' '` (a space) | Char used for filling the empty portion of the progress bar |
| template | `{prefix} {progress} {percent} ({done}/{total})` | The template of the whole line |
| prefix | `Progress:` | The leading label |
| progress | '{bar}' | The actual widget used for progress, can be `{bar}` or `{spinner}`


## Available widgets

name     | description   | type |
| ------ | ------------- | ------ |
prefix   | Leading label in default template | string
eta      | The computed ETA | datetime
tta      | The estimated remaining time (time to arrival) | timedelta
avg      | The average iteration per second | float
done     | The number of done iterations | integer
total    | The total number of iterations to be done | integer
remaing  | The number of iterations remaining to be done | integer
percent  | The percent of iterations already done | float
elapsed  | The elapsed time from the first iteration | timetuple
progress | The actual progress bar | template string (`{bar}` or `{spinner}`)

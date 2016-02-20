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

It comes with a default rendering that is enough for starting, but it's made to be
customised very easily: just writting a template string:

    bar = Bar(total=mytotalstuff, template='{prefix} {progress} ETA: {eta}')

It's just plain [python formatting](https://docs.python.org/3.4/library/string.html#formatspec)
so you can use any valid string formatting to take control over the appearance.
For example:

    bar = Bar(total=mytotalstuff, template='{progress} {percent:.2%} ETA: {eta:%H:%M:%S}')

You can also just change the fill character:

    bar = Bar(total=mytotalstuff, done_char='#')

You can change the progress logic itself, for example to use a spinner (included):

    bar = Bar(total=mytotalstuff, progress='{spinner}')
    # 'progress' kwarg must return a valid template variable.
    # included ones are {bar} and {spinner}

You can step by more than one at a time:

    for item in mystuff:
        amount = do_stuff()
        bar.update(step=amount)

You can add more template vars by subclassing `Bar`:

    class MyBar(Bar):

        @property
        def swap(self):
            return psutil.swap_memory().total

    bar = MyBar(total=20, template='{prefix} {progress} Swap usage: {swap}')

You want to compute yourself the done part?

    bar.update(done=myvar / othervar * another)

Or the target total may change during process?

    bar.update(total=newcomputedtotal)

See [examples](https://github.com/yohanboniface/progresso/blob/master/examples.py) for inspiration.

To run examples, when git cloned the repository, simply run:

    python examples.py

If you want to run only one example, add its name to the command line:

    python examples.py example_download


## Parameters

| name  | default | description |
| ----- | ------ | ------------- |
| done_char | `=` | Char used for filling the progress bar |
| remain_char | `' '` (a space) | Char used for filling the empty portion of the progress bar |
| template | `{prefix} {progress} {percent} ({done}/{total})` | The template of the whole line |
| prefix | `Progress:` | The leading label |
| animation | '{progress}' | The actual widget used for progress, can be `{bar}`, `{spinner}` or `{stream}`


## Built in template vars

name      | description   | type | default formatting
| ------  | ------------- | ------ | ---------------- |
prefix    | Leading label in default template | string | str
elapsed   | The elapsed time from the first iteration | timedelta | not formattable
eta       | The computed ETA | datetime | `%H:%M:%S` if less than 24 hours, else `%Y-%m-%d %H:%M:%S`
tta       | The estimated remaining time (time to arrival) | timedelta | not formattable
avg       | The average time per iteration, in seconds | float | `.2f`
speed     | The average number of iterations per second | float | `.2f`
done      | The number of done iterations | integer |
total     | The total number of iterations to be done | integer |
remaing   | The number of iterations remaining to be done | integer |
percent   | The percent of iterations already done | float | `.2%`
animation | The actual progress bar | template string (`{bar}`, `{spinner}` or `{stream}`) |

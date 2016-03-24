# Progressist

Minimalist and pythonic progress bar.


## Install

    pip install progressist

## Usage

    from progressist import ProgressBar
    bar = ProgressBar(total=mytotalstuff)
    for item in mystuff:
        # do_stuff
        bar.update()

Or use `bar.iter` transparently

    for item in bar.iter(mystuff):
        do_stuff

It comes with a default rendering that is enough for starting, but it's made to be
customised very easily: just writting a template string:

    bar = ProgressBar(total=mytotalstuff, template='{prefix} {progress} ETA: {eta}')

It's just plain [python formatting](https://docs.python.org/3.4/library/string.html#formatspec)
so you can use any valid string formatting to take control over the appearance.
For example:

    bar = ProgressBar(total=mytotalstuff, template='{progress} {percent:.2%} ETA: {eta:%H:%M:%S}')

You can also just change the fill character:

    bar = ProgressBar(total=mytotalstuff, done_char='#')

You can change the progress logic itself, for example to use a spinner (included):

    bar = ProgressBar(total=mytotalstuff, progress='{spinner}')
    # 'progress' kwarg must return a valid template variable.
    # included ones are {bar} and {spinner}

You can step by more than one at a time:

    for item in mystuff:
        amount = do_stuff()
        bar.update(step=amount)

You can add more template vars by subclassing `ProgressBar`:

    class MyBar(ProgressBar):

        @property
        def swap(self):
            return psutil.swap_memory().total

    bar = MyBar(total=20, template='{prefix} {progress} Swap usage: {swap}')

If you are using the same configuration at different places, create a subclass and
set its configuration as class properties:

    class MyBar(ProgressBar):
        template = ('Download |{animation}| {done:B}/{total:B}')
        done_char = '⬛'

    bar = MyBar()

You want to compute yourself the done part?

    bar.update(done=myvar / othervar * another)

Or the target total may change during process?

    bar.update(total=newcomputedtotal)

See [examples](https://github.com/yohanboniface/progressist/blob/master/examples.py) for inspiration.

To run examples, when git cloned the repository, simply run:

    python examples.py

If you want to run only one example, add its name to the command line:

    python examples.py example_download


## Parameters

You can set all of those parameters either as class properties:

    class MyBar(ProgressBar):
        done_char = 'x'

    bar = Bar()

Or at init:

    bar = ProgressBar(done_char='x')

Or at update:

    bar = Bar()
    bar.update(prefix='Finishing')

| name  | default | description |
| ----- | ------ | ------------- |
| done_char | `=` | Char used for filling the progress bar |
| remain_char | `' '` (a space) | Char used for filling the empty portion of the progress bar |
| template | `{prefix} {progress} {percent} ({done}/{total})` | The template of the whole line |
| prefix | `Progress:` | The leading label |
| animation | '{progress}' | The actual widget used for progress, can be `{bar}`, `{spinner}` or `{stream}`
| throttle | 0 | Minimum value between two `update` call to issue a render: can accept an `int` for an absolute throttling, a float for a percentage throttling (total must then be set) or a dimedelta for a throttling in seconds


## Built in template vars

name      | description   | type | default formatting
| ------  | ------------- | ------ | ---------------- |
prefix    | Leading label in default template | string | str
elapsed   | The elapsed time from the first iteration (in seconds) | int | as timedelta
eta       | The computed ETA | datetime | `%H:%M:%S` if less than 24 hours, else `%Y-%m-%d %H:%M:%S`
tta       | The estimated remaining time (time to arrival; in seconds) | int | as timedelta
avg       | The average time per iteration, in seconds | float | `.2f`
speed     | The average number of iterations per second | float | `.2f`
done      | The number of done iterations | integer |
total     | The total number of iterations to be done | integer |
remaing   | The number of iterations remaining to be done | integer |
percent   | The percent of iterations already done | float | `.2%`
animation | The actual progress bar | template string (`{bar}`, `{spinner}` or `{stream}`) |


## Custom formatting

We extend python default Formatter with some handy custom specs:

- `B` type: render an int as human friendly bytes size. For example:

        > bar.total = 109830983
        > bar.template = '{total:B}'
        > bar.render()
        '104.7 MiB'

  You can still override the ndigits value:

        > bar.total = 109830983
        > bar.template = '{total:0.2B}'
        > bar.render()
        '104.74 MiB'

- `D` type: try to cast to integer. For example:

        > bar.speed = 103.23
        > bar.template = '{speed:D}'
        > bar.render()
        '103'

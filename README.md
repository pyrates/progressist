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
| template | `\r{prefix} {progress} {percent} ({done}/{total})` | The template of the whole line |


## Available widgets

name     | description
| ------ | ------------- |
prefix   | Leading label in default template
progress | The actual progress bar
eta      | The computed ETA
lasting  | The lasting time
avg      | The average iteration per second
done     | The number of done iterations
total    | The total number of iterations to be done
remaing  | The number of iterations remaining to be done
percent  | The percent of iterations already done
elapsed  | The elapsed time from the first iteration

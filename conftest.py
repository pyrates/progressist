from time import time

import pytest

from progressist import ProgressBar


@pytest.fixture
def bar():
    return ProgressBar(total=100, columns=50, prefix='Bar:', start=time(),
                       template='{prefix} {animation} {done}/{total}')

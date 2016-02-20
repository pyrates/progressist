from time import time

import pytest

from progresso import Bar


@pytest.fixture
def bar():
    return Bar(total=100, columns=50, prefix='Bar:', start=time(),
               template='{prefix} {animation} {done}/{total}')

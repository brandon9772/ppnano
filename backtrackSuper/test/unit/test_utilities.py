import pytest

from data import Data

data = Data()


@pytest.mark.parametrize(data.test_answer())
def test_answer(
    self,
    number
):
    assert number == 5
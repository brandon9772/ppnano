import pytest

from data import Data

data = Data()
@pytest.mark.parametrize(*data.test_answer())
def test_answer(
    nanogram,
    row_counter,
    col_counter,
    condition_counter
):
    assert col_counter == 5

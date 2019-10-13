import pytest

from test.unit.data import Data
from nanogram import Nanograms
from utilities import Utilities

data = Data()
@pytest.mark.parametrize(*data.test_answer())
def test_clean_zero_max_size(
    filename,
    expected_row_condition,
    expected_col_condition,
    expected_answer,
    expected_must_cross,
):
    utilities = Utilities()
    nanograms = Nanograms('filename')
    nanograms = utilities.clean_zero_max_size(nanograms)

    expected_nanograms = Nanograms('filename')
    expected_nanograms.row_condition = expected_row_condition
    expected_nanograms.col_condition = expected_col_condition
    expected_nanograms.answer = expected_answer
    expected_nanograms.must_cross = expected_must_cross

    assert nanograms.is_equal(expected_nanograms)


@pytest.mark.parametrize(*data.test_get_next_step())
def test_answer(
    filename,
    expected_row_counter,
    expected_col_counter,
    expected_condition_counter,
):
    

    assert True

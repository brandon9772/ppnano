from pytest import param
from nanogram import Nanograms


class Data:
    def test_answer(self):
        variable = 'number'
        test_data = [
            param(
                '3',
                id='3'
            )
        ]
        return (variable, test_data)

    def test_get_next_step():
        variable = (
            'nanogram, row_counter,'
            'col_counter, condition_counter'
        )
        test_data = [
            param(
                Nanograms(r'5_5naongram_1.txt'),
                0,
                -1,
                -1,
                id='empty_all_zero_nanogram'
            )
        ]
        return (variable, test_data)
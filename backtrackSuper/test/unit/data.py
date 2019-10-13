import numpy as np
from pytest import param


class Data:
    def clean_zero_max_size(self):
        variable = (
            'filename,'
            'expected_row_condition_change,'
            'expected_col_condition_change,'
            'expected_answer,'
            'expected_must_cross'
        )
        test_data = [
            param(
                'nanogram/all_one_5x5.txt',
                [],
                [],
                np.zeros((self.col_size), dtype=self.dtype),
                np.full(
                    (self.col_size), ~0 >> self.row_size << self.row_size,
                    dtype=self.dtype
                ),
                id='only_1_from_start_nanogram'
            )
        ]
        return (variable, test_data)

    def get_next_step(self):
        variable = 'filename, expected_filename'
        test_data = [
            param(
                'nanogram/no_change.txt',
                'expected_nanogram/no_change.txt',
                id='no_change'
            )
        ]
        return (variable, test_data)

import copy
import numpy as np


class Utilities:
    def clean_zero_max_size(self, nanogram):
        row_size = nanogram.row_size
        col_size = nanogram.col_size
        all_one = np.asarray([~0], dtype=nanogram.dtype)
        full_row = np.right_shift(all_one[0], nanogram.dtype_size-row_size)
        for (i, condition) in enumerate(nanogram.row_condition):
            if len(condition) != 1:
                continue
            if condition[0][0] == 0:
                nanogram.must_cross[i] = ~0
            if condition[0][0] == row_size:
                nanogram.answer[i] = full_row
        for (i, condition) in enumerate(nanogram.col_condition):
            if len(condition) != 1:
                continue
            if condition[0][0] == 0:
                add_bit = 1 << i
                for j in range(col_size):
                    nanogram.must_cross[j] = (
                        nanogram.must_cross[j] | add_bit
                    )
            if condition[0][0] == col_size:
                add_bit = 1 << i
                for j in range(col_size):
                    nanogram.answer[j] = (
                        nanogram.answer[j] | add_bit
                    )
        return nanogram

    def get_next_step(self, nanogram, all_counter):
        if not all_counter:
            raise ValueError('this nanogram has no solution')
        row_counter = all_counter[-1][0]
        col_counter = all_counter[-1][1]
        condition_counter = all_counter[-1][2]

        max_col_counter = -1

        for condition in nanogram.row_condition[
            row_counter
        ][condition_counter:]:
            max_col_counter += condition[0] + 1

        max_col_counter = nanogram.row_size - max_col_counter

        if not col_counter > max_col_counter:
            all_counter[-1][1] += 1
            return all_counter
        all_counter = all_counter[:-1]
        return self.get_next_step(nanogram, all_counter)

    def chain_fill(self, nanogram, counter, right_cross_min=-1):
        nanogram = copy.deepcopy(nanogram)
        row_counter = counter[0]
        col_counter = counter[1]
        condition_counter = counter[2]
        dtype_size = nanogram.dtype_size
        row_size = nanogram.row_condition[row_counter][condition_counter][0]
        #fill row
        row_fill = np.left_shift(
            (
                np.right_shift(
                    np.asarray([~0], dtype=nanogram.dtype)[0],
                    dtype_size - row_size
                )
            ),
            col_counter
        )
        nanogram.answer[row_counter] = nanogram.answer[row_counter] | row_fill
        left_cross = 1 << col_counter+1
        right_cross = np.left_shift(
            (
                np.right_shift(
                    np.asarray([~0], dtype=nanogram.dtype)[0],
                    dtype_size - col_counter + right_cross_min + 1
                )
            ),
            right_cross_min + 1
        )
        cross = left_cross | right_cross
        nanogram.must_cross[row_counter] = (
            nanogram.must_cross[row_counter] | cross
        )

        if condition_counter == len(nanogram.row_condition[row_counter]) - 1:
            all_left_cross = ~0 << col_counter+row_size
            nanogram.must_cross[row_counter] = (
                nanogram.must_cross[row_counter] | all_left_cross
            )
        nanogram.row_condition[row_counter][condition_counter][1] = True
        # fill col
        for (col_index, condition) in enumerate(nanogram.col_condition[
            col_counter: col_counter+row_size
        ]):
            for (condition_index, each_condition) in enumerate(condition):
                if not each_condition[1]:
                    # fill column
                    bit_cross = 1 << col_index
                    for row_index in range(
                        row_counter,
                        row_counter + each_condition[0]
                    ):
                        nanogram.answer[row_index] = (
                           nanogram.answer[row_index] | bit_cross
                        )
                    nanogram.col_condition[
                        col_index
                    ][condition_index][1] = True
                    cross_bottom_index = row_counter + each_condition[0]
                    if cross_bottom_index < nanogram.col_size:
                        cross_bottom = 1 << col_index
                        nanogram.must_cross[cross_bottom_index] = (
                            nanogram.must_cross[cross_bottom_index]
                            | cross_bottom
                        )
                        pass

        return nanogram
        
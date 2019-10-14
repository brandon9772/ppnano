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
            if condition[0] == 0:
                nanogram.must_cross[i] = ~0
            if condition[0] == row_size:
                nanogram.answer[i] = full_row
                nanogram.row_condition_bool[i][0] = True
        for (i, condition) in enumerate(nanogram.col_condition):
            if len(condition) != 1:
                continue
            if condition[0] == 0:
                add_bit = 1 << i
                for j in range(col_size):
                    nanogram.must_cross[j] = (
                        nanogram.must_cross[j] | add_bit
                    )
            if condition[0] == col_size:
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

        if col_counter == -1:
            all_counter[-1][1] = 0
            return all_counter

        max_col_counter = -1

        for condition in nanogram.row_condition[
            row_counter
        ][condition_counter:]:
            max_col_counter += condition + 1

        max_col_counter = nanogram.row_size - max_col_counter

        if not col_counter > max_col_counter:
            all_counter[-1][1] += 1
            condition_size = nanogram.row_condition[row_counter][condition_counter]
            if nanogram.must_cross[row_counter] & (
                np.left_shift(
                    np.right_shift(
                        nanogram.all_one,
                        nanogram.dtype_size - condition_size
                    ),
                    col_counter + 1
                )
            ):
                return self.get_next_step(nanogram, all_counter)
            if nanogram.answer[row_counter] & (1 << col_counter):
                return self.get_next_step(nanogram, all_counter)
            if nanogram.answer[row_counter] & (1 << col_counter + condition_size + 1):
                return self.get_next_step(nanogram, all_counter)
            return all_counter
        all_counter = all_counter[:-1]
        return self.get_next_step(nanogram, all_counter)

    def chain_fill(self, origin_nanogram, counter, right_cross_min=-1):
        # nanogram = copy.deepcopy(origin_nanogram)
        nanogram = origin_nanogram.copy()
        row_counter = counter[0]
        col_counter = counter[1]
        condition_counter = counter[2]
        dtype_size = nanogram.dtype_size
        row_size = nanogram.row_condition[row_counter][condition_counter]
        # fill row
        row_fill = np.left_shift(
            (
                np.right_shift(
                    nanogram.all_one,
                    dtype_size - row_size
                )
            ),
            col_counter
        )
        finish_col = nanogram.answer[row_counter] & row_fill
        nanogram.answer[row_counter] = nanogram.answer[row_counter] | row_fill
        left_cross = 1 << col_counter + row_size
        right_cross = np.left_shift(
            (
                np.right_shift(
                    nanogram.all_one,
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
        nanogram.row_condition_bool[row_counter][condition_counter] = True
        # fill col
        max_col_size = 0
        for (col_index, condition) in enumerate(nanogram.col_condition[
            col_counter: col_counter+row_size
        ]):
            if finish_col & (1 << col_index + col_counter):
                continue
            not_possible = True
            for (condition_index, each_condition) in enumerate(condition):
                if not nanogram.col_condition_bool[col_index + col_counter][condition_index]:
                    not_possible = False
                    max_col_size = max(max_col_size, each_condition)
                    # fill column
                    bit_cross = 1 << col_index + col_counter
                    for row_index in range(
                        row_counter,
                        row_counter + each_condition
                    ):
                        nanogram.answer[row_index] = (
                            nanogram.answer[row_index] | bit_cross
                        )
                    nanogram.col_condition_bool[
                        col_index +
                        col_counter
                    ][condition_index] = True
                    cross_bottom_index = row_counter + each_condition
                    if cross_bottom_index < nanogram.col_size:
                        nanogram.must_cross[cross_bottom_index] = (
                            nanogram.must_cross[cross_bottom_index]
                            | bit_cross
                        )
                    break
            if not_possible:
                raise ValueError('impossible')
        return (
            nanogram,
            row_counter,
            row_counter + row_size,
            col_counter,
            col_counter + max_col_size + 1
        )

    @profile
    def is_possible(
        self,
        nanogram,
        row_start,
        row_end,
        col_start,
        col_end
    ):
        for (fill, cross) in zip(
            nanogram.answer, nanogram.must_cross
        ):
            if (fill & cross) != 0:
                return False
        if row_start < 0:
            row_start = 0
        elif row_start > nanogram.col_size:
            row_start = nanogram.col_size
        if row_end < 0:
            row_end = 0
        elif row_end > nanogram.col_size:
            row_end = nanogram.col_size
        for row in range(row_start, row_end):
            cross = nanogram.must_cross[row]
            condition_list = nanogram.row_condition[row]
            streak_list = []
            streak = 0
            for i in bin(cross):
                if i:
                    streak += 1
                else:
                    if streak != 0:
                        streak_list.append(streak)
                        streak = 0
            if streak != 0:
                streak_list.append(streak)

            streak_counter = 0
            max_streak_counter = len(streak_list)
            for condition in condition_list:
                diff = streak_list[streak_counter] - condition
                while(diff < 0):
                    streak_counter += 1
                    if streak_counter == max_streak_counter:
                        return False
                    diff = streak_list[streak_counter] - condition
                streak_list[streak_counter] = diff - 1

        if col_start < 0:
            col_start = 0
        elif col_start > nanogram.row_size:
            col_start = nanogram.row_size
        if col_end < 0:
            col_end = 0
        elif col_end > nanogram.row_size:
            col_end = nanogram.row_size
        for col in range(col_start, col_end):
            cross = nanogram.get_col_must_cross(col)
            condition_list = nanogram.col_condition[col]
            streak_list = []
            streak = 0
            for i in range(nanogram.col_size):
                if not cross & (1 << i):
                    streak += 1
                else:
                    if streak != 0:
                        streak_list.append(streak)
                        streak = 0
            if streak != 0:
                streak_list.append(streak)
            streak_counter = 0

            max_streak_counter = len(streak_list)
            for condition in condition_list:
                diff = streak_list[streak_counter] - condition
                while(diff < 0):
                    streak_counter += 1
                    if streak_counter == max_streak_counter:
                        return False
                    diff = streak_list[streak_counter] - condition
                streak_list[streak_counter] = diff - 1

        return True

    def get_next_condition(self, nanogram, counter):
        next_counter = copy.deepcopy(counter)
        same_row = True
        next_counter[2] += 1
        while(next_counter[2] >= len(nanogram.row_condition[counter[0]])):
            next_counter[0] += 1
            next_counter[1] = -1
            next_counter[2] = 0
            same_row = False
        if same_row:
            next_col = (
                nanogram.row_condition[counter[0]][counter[2]]
                + counter[1]
            )
            next_counter[1] = next_col
        return next_counter

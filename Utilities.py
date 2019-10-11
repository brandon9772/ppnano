import numpy as np


class Utilities():

    def fill_array_from_start_to_end(self, start, end, size):
        return np.asarray([0]*start + [1]*(end-start) + [0]*(size-end))

    def get_first_and_last_true(potential, condition_size):
        answer = []
        for (key, value) in enumerate(potential):
            if value:
                answer.append(key)
                break
        for (key, value) in enumerate(reversed(potential)):
            if value:
                answer.append(len(potential) - key - 1 + condition_size)
                break
        return answer

    def set_true_must_fill_start_end(
        self,
        nanograms,
        index,
        start,
        end,
        isRow
    ):
        if isRow:
            nanograms.must_fill[index, start:end] = True
        else:
            nanograms.must_fill[start:end, index] = True
        return nanograms

    def set_true_must_cross_full_potential(
        self,
        nanograms,
        index,
        full_potential,
        isRow
    ):
        if isRow:
            for (potential_index, potential_value) in enumerate(
                    full_potential
            ):
                if not potential_value:
                    nanograms.must_cross[index][potential_index] = True
        else:
            for (potential_index, potential_value) in enumerate(
                    full_potential
            ):
                if not potential_value:
                    nanograms.must_cross[potential_index][index] = True
        return nanograms

    def update_to_must_fill_must_cross_line(self, nanograms, isRow):
        condition_potential = None
        line_condition = None
        if isRow:
            condition_potential = nanograms.row_condition_potential
            line_condition = nanograms.row_condition
        else:
            condition_potential = nanograms.col_condition_potential
            line_condition = nanograms.col_condition

        for (index, value) in enumerate(condition_potential):
            # get all fillable box for must cross
            full_potential = np.zeros((nanograms.row_size), dtype=bool)
            # for each condition within the line
            for (condition_index, condition_value) in enumerate(value):
                streak_start = 0
                streak = False
                condition_size = line_condition[index][condition_index]
                # get earliest start and latest start for must fill
                earliest_start = None
                lastest_start = None
                for (each_condition_index, each_condition_value) in enumerate(
                    condition_value
                ):
                    if each_condition_value:
                        if streak:
                            continue
                        else:
                            if earliest_start is None:
                                earliest_start = each_condition_index
                            streak = True
                            streak_start = each_condition_index
                    else:
                        if streak:
                            full_potential[
                                streak_start:
                                each_condition_index+condition_size-1
                            ] = True
                            lastest_start = each_condition_index - 1
                            streak = False
                        continue
                if streak:
                    full_potential[streak_start:] = True
                    lastest_start = len(condition_value)
                nanograms = self.set_true_must_fill_start_end(
                    nanograms,
                    index,
                    lastest_start,
                    earliest_start+condition_size,
                    isRow
                )
            nanograms = self.set_true_must_cross_full_potential(
                nanograms,
                index,
                full_potential,
                isRow
            )
        return nanograms

    # main
    def update_to_must_fill_must_cross(self, nanograms):
        nanograms = self.update_to_must_fill_must_cross_line(
            nanograms,
            True
        )
        return self.update_to_must_fill_must_cross_line(nanograms, False)

    def get_must_fill_ij(self, nanogram, i, j):
        return nanogram.must_fill[i][j]

    def get_must_fill_ji(self, nanogram, i, j):
        return nanogram.must_fill[j][i]

    def set_must_cross_row(self, nanogram, index, i, j):
        nanogram.must_cross[index, i:j] = True
        return nanogram

    def set_must_cross_col(self, nanogram, index, i, j):
        nanogram.must_cross[i:j, index] = True
        return nanogram

    def update_from_must_fill_line(
        self,
        nanogram,
        isRow,
        start_line=0,
        end_line=None,
    ):
        if end_line is None:
            if isRow:
                end_line = nanogram.row_size
            else:
                end_line = nanogram.col_size

        size_j_range = None
        get_mustfill = None

        if isRow:
            size_j_range = [0, nanogram.col_size]
            get_mustfill = self.get_must_fill_ij
        else:
            size_j_range = [0, nanogram.row_size]
            get_mustfill = self.get_must_fill_ji
        if isRow:
            for i in range(start_line, end_line):
                streak_start = False
                streak_dict = {}
                streak = 0
                # get streak and cross start within streak
                for j in range(size_j_range[0], size_j_range[1]):
                    if get_mustfill(nanogram, i, j):
                        if not streak_start:
                            streak_start = True
                        streak += 1
                    else:
                        if streak_start:
                            streak_start = False
                            streak_dict[j-streak] = streak
                            streak = 0
                if streak_start:
                    streak_start = False
                    streak_dict[j-streak] = streak
                    streak = 0
                # cross start that end condition within streak.
                for (index, j) in enumerate(nanogram.row_condition[i]):
                    for (streak_start, streak) in streak_dict.items():
                        nanogram.row_condition_potential[
                            i
                        ][
                            index
                        ][
                            max(streak_start - j, 0):
                            max(
                                min(
                                    streak_start - 2,
                                    streak_start + streak - j - 1
                                ),
                                0
                            )
                        ] = False
                earliest_start = 0
                # The must be before this must fill rule.
                # all consequences is accounted for.
                # at index is accounted for.
                # before index is accounted for.
                # after index is accounted for.
                for (streak_start, streak) in streak_dict.items():
                    start = earliest_start
                    for (index, j) in enumerate(nanogram.row_condition[i]):
                        start += j + 1
                        if streak_start <= start:
                            earliest_start = max(
                                start + 1,
                                streak_start + streak + 1
                            )
                            nanogram.row_condition_potential[
                                i
                            ][
                                index
                            ][
                                streak_start+1:
                            ] = False
                            nanogram.row_condition_potential[
                                i
                            ][
                                index
                            ][
                                :streak_start
                            ] = False
                            if index == len(nanogram.row_condition[i]) - 1:
                                break
                            for k in range(
                                index+1,
                                len(nanogram.row_condition[i])
                            ):
                                nanogram.row_condition_potential[
                                    i
                                ][
                                    k
                                ][
                                    :streak_start+streak
                                ] = False
                            for k in range(0, index):
                                nanogram.row_condition_potential[
                                    i
                                ][
                                    k
                                ][
                                    streak_start+1:
                                ] = False
                            break
        else:
            for i in range(start_line, end_line):
                streak_start = False
                streak_dict = {}
                streak = 0
                # get streak and cross start within streak
                for j in range(size_j_range[0], size_j_range[1]):
                    if get_mustfill(nanogram, i, j):
                        if not streak_start:
                            streak_start = True
                        streak += 1
                    else:
                        if streak_start:
                            streak_start = False
                            streak_dict[j-streak] = streak
                            streak = 0
                if streak_start:
                    streak_start = False
                    streak_dict[j-streak] = streak
                    streak = 0
                # cross start that end condition within streak.
                for (index, j) in enumerate(nanogram.col_condition[i]):
                    for (streak_start, streak) in streak_dict.items():
                        nanogram.col_condition_potential[
                            i
                        ][
                            index
                        ][
                            max(streak_start - j, 0):
                            max(
                                min(
                                    streak_start - 2,
                                    streak_start + streak - j - 1
                                ),
                                0
                            )
                        ] = False

                # The start must be before this must fill rule.
                # all consequences is accounted for.
                # at index is accounted for.
                # before index is accounted for.
                # after index is accounted for.
                start = 0
                for (streak_start, streak) in streak_dict.items():
                    for (index, j) in enumerate(nanogram.col_condition[i]):
                        start += j + 1
                        if streak_start <= start:
                            start = max(
                                start + 1,
                                streak_start + streak + 1
                            )
                            nanogram.col_condition_potential[
                                i
                            ][
                                index
                            ][
                                streak_start+1:
                            ] = False
                            nanogram.col_condition_potential[
                                i
                            ][
                                index
                            ][
                                :streak_start
                            ] = False
                            if index == len(nanogram.col_condition[i]) - 1:
                                break
                            for k in range(
                                index+1,
                                len(nanogram.col_condition[i])
                            ):
                                nanogram.col_condition_potential[
                                    i
                                ][
                                    k
                                ][
                                    :streak_start+streak
                                ] = False
                            for k in range(0, index):
                                nanogram.col_condition_potential[
                                    i
                                ][
                                    k
                                ][
                                    streak_start+1:
                                ] = False
                            break
        return nanogram

    # main
    def update_from_must_fill(
        self,
        nanogram,
        start_row=0,
        end_row=None,
        start_col=0,
        end_col=None,
    ):
        nanogram = self.update_from_must_fill_line(
            nanogram,
            True,
            start_row,
            end_row
        )
        return self.update_from_must_fill_line(
            nanogram,
            False,
            start_col,
            end_col
        )

import numpy as np
from Utilities import Utilities


class Nanograms:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.utilities = Utilities()

        self.row_size = int(f.readline())
        self.col_size = int(f.readline())

        self.row_condition = []
        self.row_condition_potential = []
        self.col_condition = []
        self.col_condition_potential = []

        def get_condition_potential(condition):
            end = self.row_size - sum(condition) - len(condition) + 2
            start = 0
            condition_potential = []
            for i in condition:
                condition_potential.append(
                    self.utilities.fill_array_from_start_to_end(
                        start, end, self.row_size
                    )
                )
                start += i + 1
                end += i + 1
            return condition_potential

        for _ in range(self.row_size):
            condition = [int(x) for x in f.readline().split(' ')]
            self.row_condition.append(condition)
            self.row_condition_potential.append(
                get_condition_potential(condition)
            )
        for _ in range(self.col_size):
            condition = [int(x) for x in f.readline().split(' ')]
            self.col_condition.append(condition)
            self.col_condition_potential.append(
                get_condition_potential(condition)
            )
        f.close()

        self.row_condition_potential = [
            [
                np.asarray(y, dtype=bool) for y in x
            ] for x in self.row_condition_potential
        ]
        self.col_condition_potential = [
            [
                np.asarray(y, dtype=bool) for y in x
            ] for x in self.col_condition_potential
        ]

        emptyArray = np.zeros((self.row_size, self.col_size), dtype=bool)
        self.current_answer = [emptyArray.copy()]
        self.must_fill = emptyArray.copy()
        self.must_cross = emptyArray.copy()

    def printAnsFillCross(self):
        print('answer')
        print(list(self.current_answer))
        print()
        print('must_fill')
        print(list(self.must_fill))
        print()
        print('must_cross')
        print(list(self.must_cross))
        print()
        print('row_condition_potential')
        print(list(self.row_condition_potential))
        print()
        print('col_condition_potential')
        print(list(self.col_condition_potential))
        print()

    def nanogram_equal(self, nanogram):
        if not np.array_equal(self.must_fill, nanogram.must_fill):
            return False
        if not np.array_equal(self.must_cross, nanogram.must_cross):
            return False
        if (
            len(self.row_condition_potential) !=
            len(nanogram.row_condition_potential)
        ):
            return False
        for (self_rcp, nano_rcp) in zip(
            self.row_condition_potential,
            nanogram.row_condition_potential
        ):
            if (
                len(self_rcp) !=
                len(nano_rcp)
            ):
                return False
            for (self_np_array, nano_np_array) in zip(
                self_rcp,
                nano_rcp
            ):
                if not np.array_equal(self_np_array, nano_np_array):
                    return False
        if (
            len(self.col_condition_potential) !=
            len(nanogram.col_condition_potential)
        ):
            return False
        for (self_ccp, nano_ccp) in zip(
            self.col_condition_potential,
            nanogram.col_condition_potential
        ):
            if (
                len(self_ccp) !=
                len(nano_ccp)
            ):
                return False
            for (self_np_array, nano_np_array) in zip(
                self_ccp,
                nano_ccp
            ):
                if not np.array_equal(self_np_array, nano_np_array):
                    return False
        return True

    def getAnswer(self):
        answer_arr = np.zeros((self.row_size, self.col_size), dtype=bool)
        is_solve = True
        for (index, row) in enumerate(self.row_condition_potential):
            solve = False
            start = None
            for (row_index, condition) in enumerate(row):
                for value in condition:
                    if value:
                        if not solve:
                            start = row_index
                            solve = True
                        else:
                            solve = False
                            start = None
                            is_solve = False
                            break
                if start is not None:
                    answer_arr[index][
                        start: start+self.row_condition[index][row_index]
                    ] = True
        return [is_solve, answer_arr]

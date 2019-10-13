import numpy as np


class Nanograms:
    def __init__(self, filename=None):
        if filename is None:
            self.row_size = None
            self.col_size = None
            self.row_condition = None
            self.col_condition = None
            self.dtype = None
            self.dtype_size = None
            self.answer = None
            self.must_cross = None
            return
        f = open(filename, 'r')

        # int
        self.row_size = int(f.readline())
        self.col_size = int(f.readline())

        # [[[int: bool]]]
        self.row_condition = []
        self.col_condition = []

        if self.row_size > 64 or self.col_size > 64:
            raise ValueError(
                "can't solve nanograms greater than 64 on either size"
            )
        if self.row_size > 32 or self.col_size > 32:
            self.dtype = 'uint64'
            self.dtype_size = 64
        elif self.row_size > 16 or self.col_size > 16:
            self.dtype = 'uint32'
            self.dtype_size = 32
        elif self.row_size > 8 or self.col_size > 8:
            self.dtype = 'uint16'
            self.dtype_size = 16
        else:
            self.dtype = 'uint8'
            self.dtype_size = 8

        for _ in range(self.row_size):
            condition = [[int(x), False] for x in f.readline().split(' ')]
            condition.reverse()
            self.row_condition.append(condition)

        for _ in range(self.col_size):
            condition = [[int(x), False] for x in f.readline().split(' ')]
            self.col_condition.append(condition)
        self.col_condition.reverse()
        f.close()

        # step:
        # [[row_counter, col_counter, condition_counter]]
        self.answer = np.zeros((self.col_size), dtype=self.dtype)
        self.must_cross = np.full(
                (self.col_size), ~0 >> self.row_size << self.row_size,
                dtype=self.dtype
            )

    def is_equal(self, nanograms):
        if self.row_size != nanograms.row_size:
            return False
        if self.col_size != nanograms.col_size:
            return False
        if self.dtype != nanograms.dtype:
            return False
        if self.dtype_size != nanograms.dtype_size:
            return False
        if self.row_condition != nanograms.row_condition:
            return False
        if self.col_condition != nanograms.col_condition:
            return False
        if not np.array_equal(self.answer, nanograms.answer):
            return False
        if not np.array_equal(self.must_cross, nanograms.must_cross):
            return False
        return True

    def print_all(self):
        print(f'row size: {self.row_size}')
        print(f'col size: {self.col_size}')
        print('row condition:')
        print(self.row_condition)
        print('col condition:')
        print(self.col_condition)

        print('answer')
        for ans in self.answer:
            print(np.binary_repr(ans, width=self.row_size))
        print('must_cross')
        for cross in self.must_cross:
            print(
                str(
                    np.binary_repr(cross, width=self.row_size)
                )[self.dtype_size-self.col_size:]
            )
        self.print_answer_must_cross()

    def print_answer_must_cross(self):
        out = np.empty((self.col_size, self.row_size), dtype=str)
        row = 0
        for (ans, cross) in zip(self.answer, self.must_cross):
            ans = map(int, str(np.binary_repr(ans, width=self.row_size)))
            cross = map(
                int,
                str(
                    np.binary_repr(
                        cross,
                        width=self.row_size
                    )
                )[self.dtype_size-self.col_size:]
            )
            col = 0
            for (ans_cell, cross_cell) in zip(ans, cross):
                if ans_cell == 1 and cross_cell == 1:
                    out[row, col] = '!'
                elif ans_cell == 1 and cross_cell == 0:
                    out[row, col] = 'X'
                elif ans_cell == 0 and cross_cell == 1:
                    out[row, col] = 'O'
                elif ans_cell == 0 and cross_cell == 0:
                    out[row, col] = '_'
                col += 1
            row += 1
        for row_out in out:
            row_str = ''
            for cell_row_out in row_out:
                row_str += cell_row_out + ' '
            print(row_str)




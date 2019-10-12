import numpy as np


class Nanograms:
    def __init__(self, filename):
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
            self.row_condition.append(condition)

        for _ in range(self.col_size):
            condition = [[int(x), False] for x in f.readline().split(' ')]
            self.col_condition.append(condition)
        f.close()

        # step:
        # [[row_counter, col_counter, condition_counter]]
        self.answer = np.zeros((self.col_size), dtype=self.dtype)
        self.must_cross = np.full(
                (self.col_size), ~0 >> self.row_size << self.row_size,
                dtype=self.dtype
            )

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

    def print_answer_must_cross(self):
        out = np.empty((self.col_size, self.row_size), dtype=str)
        row = 0
        for (ans, cross) in zip(self.answer, self.must_cross):
            ans = map(int, str(np.binary_repr(ans, width=self.row_size)))
            cross = map(
                int,
                str(np.binary_repr(
                    cross, width=self.row_size)
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




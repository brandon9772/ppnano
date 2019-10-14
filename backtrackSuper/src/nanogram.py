import copy
import numpy as np


class Nanograms:
    def __init__(self, filename=None):
        if filename is None:
            # self.row_size = None
            # self.col_size = None
            # self.row_condition = None
            # self.col_condition = None
            # self.row_condition_bool = None
            # self.col_condition_bool = None
            # self.dtype = None
            # self.dtype_size = None
            # self.answer = None
            # self.must_cross = None
            return
        f = open(filename, 'r')

        # int
        self.col_size = int(f.readline())
        self.row_size = int(f.readline())

        # [[[int: bool]]]
        self.row_condition = []
        self.col_condition = []
        self.row_condition_bool = []
        self.col_condition_bool = []

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

        for _ in range(self.col_size):
            condition = [int(x) for x in f.readline().split(' ')]
            condition_bool = [False for _ in condition]
            condition.reverse()
            condition_bool.reverse()
            self.row_condition.append(condition)
            self.row_condition_bool.append(condition_bool)

        for _ in range(self.row_size):
            condition = [int(x) for x in f.readline().split(' ')]
            condition_bool = [False for _ in condition]
            self.col_condition.append(condition)
            self.col_condition_bool.append(condition_bool)
        self.col_condition.reverse()
        self.col_condition_bool.reverse()
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
        if self.row_condition_bool != nanograms.row_condition_bool:
            return False
        if self.col_condition_bool != nanograms.col_condition_bool:
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
        print('row condition bool:')
        print(self.row_condition_bool)
        print('col condition bool:')
        print(self.col_condition_bool)

        print('answer')
        for ans in self.answer:
            print(np.binary_repr(ans, width=self.row_size))
        print('must_cross')
        for cross in self.must_cross:
            print(
                str(
                    np.binary_repr(cross, width=self.row_size)
                )[self.dtype_size-self.row_size:]
            )
        self.print_answer_must_cross()

    def print_answer_must_cross(self):
        out = np.empty((self.col_size, self.row_size), dtype=str)
        row = 0
        max_col_header_size = 0
        max_row_header_size = 0

        for col_condition in self.col_condition:
            max_col_header_size = max(max_col_header_size, len(col_condition))
        for row_condition in self.row_condition:
            max_row_header_size = max(max_row_header_size, len(row_condition))

        col_header = [
            [
                '  ' for _ in range(self.row_size)
            ]for _ in range(max_col_header_size)
        ]
        for (col_index, col_condition) in enumerate(reversed(self.col_condition)):
            for (condition_index, condition) in enumerate(reversed(col_condition)):
                if condition < 10:
                    col_header[condition_index][col_index] = ' ' + \
                        str(condition)
                else:
                    col_header[condition_index][col_index] = str(condition)
        for headers in reversed(col_header):
            col_header_str = (max_row_header_size)*'   ' + '  '
            for each_line_header in headers:
                col_header_str += each_line_header + ' '
            print(col_header_str)
        print(max_row_header_size * '   ' + (self.row_size + 1) * '---')
        row_header = [
            [
                '  ' for _ in range(max_row_header_size)
            ]for _ in range(self.col_size)
        ]
        for (row_index, row_condition) in enumerate(self.row_condition):
            for (condition_index, condition) in enumerate(row_condition):
                if condition < 10:
                    row_header[row_index][condition_index] = ' ' + \
                        str(condition)
                else:
                    row_header[row_index][condition_index] = str(condition)

        for (ans, cross) in zip(self.answer, self.must_cross):
            ans = list(map(int, str(np.binary_repr(ans, width=self.row_size))))
            cross = list(map(
                int,
                str(
                    np.binary_repr(
                        cross,
                        width=self.row_size
                    )
                )[self.dtype_size-self.row_size:]
            ))
            col = 0
            for (ans_cell, cross_cell) in zip(ans, cross):
                if ans_cell == 1 and cross_cell == 1:
                    out[row, col] = '!'
                elif ans_cell == 1 and cross_cell == 0:
                    out[row, col] = chr(9632)
                elif ans_cell == 0 and cross_cell == 1:
                    out[row, col] = 'x'
                elif ans_cell == 0 and cross_cell == 0:
                    out[row, col] = '_'
                col += 1
            row += 1
        for (header, row_out) in zip(row_header, out):
            row_str = ''
            for each_header in reversed(header):
                row_str = row_str + each_header + ' '
            row_str += ' | '
            for cell_row_out in row_out:
                row_str += cell_row_out + '  '
            print(row_str)

    def copy(self):
        nanogram = Nanograms()
        nanogram.row_size = self.row_size
        nanogram.col_size = self.col_size
        nanogram.row_condition = self.row_condition
        nanogram.col_condition = self.col_condition
        nanogram.row_condition_bool = [
            [
                each_condition for each_condition in row
            ] for row in self.row_condition_bool
        ]
        nanogram.col_condition_bool = [
            [
                each_condition for each_condition in col
            ] for col in self.col_condition_bool
        ]
        nanogram.dtype = self.dtype
        nanogram.dtype_size = self.dtype_size
        nanogram.answer = self.answer.copy()
        nanogram.must_cross = self.must_cross.copy()
        return nanogram

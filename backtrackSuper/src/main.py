from nanogram import Nanograms
from solver import Solver
from utilities import Utilities

# filename = r'D:\python\nanogram\question\question1_5x5.txt'
filename = (r'D:\python\nanogram\ppnano\backtrackSuper'
            r'\test\unit\nanogram\test_q_1_chain_fill_5x5.txt')
nanogram = Nanograms(filename)
utilities = Utilities()
solver = Solver(utilities)

all_counter = [[0, -1, 0]]

nanogram = utilities.clean_zero_max_size(nanogram)
answer = None
step_answer = [nanogram]
last_counter = [
    nanogram.row_size-1,
    nanogram.col_size-1,
    len(nanogram.row_condition[-1]) - 1
]

# loop
iteratuin = 0
while(iteratuin < 1):
    iteratuin += 1
    all_counter = utilities.get_next_step(nanogram, all_counter)
    step_answer = step_answer[:len(all_counter)]
    next_nanogram = utilities.chain_fill(step_answer[-1], all_counter[-1])
    next_nanogram.print_all()
    break
    if utilities.is_possible(next_nanogram):
        step_answer.append(next_nanogram)
        utilities.get_next_condition(nanogram, all_counter)
        if all_counter[-1] == last_counter:
            next_nanogram.print_all()
            print('solved')
            break
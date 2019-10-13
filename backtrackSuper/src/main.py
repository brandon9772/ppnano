from nanogram import Nanograms
from solver import Solver
from utilities import Utilities

# filename = r'D:\python\nanogram\question\question1_5x5.txt'
filename = (r'D:\python\nanogram\ppnano\backtrackSuper'
            r'\test\unit\nanogram\test_q_2_chain_fill_5x5.txt')
nanogram = Nanograms(filename)
utilities = Utilities()
solver = Solver(utilities)

all_counter = [[0, -1, 0]]

nanogram = utilities.clean_zero_max_size(nanogram)
answer = None
step_answer = [nanogram]
last_counter = [
    nanogram.row_size-1,
    len(nanogram.row_condition[-1]) - 1
]

# loop
iteration = 0
next_nanogram = None
while(iteration < 50):
    print('------------------')
    print(iteration)
    print(all_counter)
    print(len(step_answer))
    print('-----')
    iteration += 1
    all_counter = utilities.get_next_step(nanogram, all_counter)
    print('next step')
    print(all_counter)
    print('------------------')
    step_answer = step_answer[:len(all_counter)]
    possible = True
    try:
        if all_counter[-1] == [2, 4, 1]:
            step_answer[-1].print_all()
        right_cross_min = -1
        if all_counter[-1][2] > 0:
            right_cross_min = all_counter[-2][1]
        next_nanogram = utilities.chain_fill(
            step_answer[-1],
            all_counter[-1],
            right_cross_min
        )
        next_nanogram.print_all()
        possible = utilities.is_possible(next_nanogram)
    except Exception as e:
        print(e)
        possible = False
    if possible:
        next_nanogram.print_all()
        step_answer.append(next_nanogram)
        if (
            all_counter[-1][0] == last_counter[0] and
            all_counter[-1][2] == last_counter[2]
        ):
            next_nanogram.print_all()
            print('solved')
            break
        next_counter = utilities.get_next_condition(nanogram, all_counter[-1])
        all_counter.append(next_counter)

step_answer[-1].print_all()

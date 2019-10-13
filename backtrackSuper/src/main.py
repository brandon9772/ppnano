from nanogram import Nanograms
from solver import Solver
from utilities import Utilities
import time

# python "D:\python\conda\envs\brandon\Lib\site-packages\kernprof.py" -l -v D:\python\nanogram\ppnano\backtrackSuper\src\main.py

filename_list = [
    (
        r'backtrackSuper'
        r'\test\unit\nanogram\test_q_2_chain_fill_5x5.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_1_5x5.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_2_5x5.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_1_10x10.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_2_10x10.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_3_10x10.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_1_15x15.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_2_15x15.txt'
    ),
    (
        r'backtrackSuper'
        r'\question\q_3_15x15.txt'
    ),
    # (
    #     r'backtrackSuper'
    #     r'\question\q_1_25x25.txt'
    # ),
]

time_list = []
solved_list = []
answer_dict = {}

utilities = Utilities()
solver = Solver(utilities)
max_iteration = 4000

for filename in filename_list:
    start = time.time()
    print(filename)
    nanogram = Nanograms(filename)
    try:
        answer = solver.solve_nanogram(nanogram, max_iteration)
        answer[0].print_all()
        answer_dict[filename] = answer
        solved_list.append('solved')
        print('solved')
    except Exception as e:
        print(e)
        answer_dict[filename] = [None, None]
        solved_list.append('unsolvable')
        print('unsolvable')
    end = time.time() - start
    time_list.append(end)

for (time_taken, filename, solve) in zip(
    time_list,
    filename_list,
    solved_list
):
    print(
        f'{filename}: iteration: {answer_dict[filename][1]}, {time_taken} second. {solve}'
    )

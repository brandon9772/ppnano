from nanogram import Nanograms
from solver import Solver
from utilities import Utilities

# filename = r'D:\python\nanogram\question\question1_5x5.txt'
filename_list = [
    (
        r'D:\python\nanogram\ppnano\backtrackSuper'
        r'\test\unit\nanogram\test_q_2_chain_fill_5x5.txt'
    )
]

utilities = Utilities()
solver = Solver(utilities)

for filename in filename_list:
    nanogram = Nanograms(filename)
    try:
        answer = solver.solve_nanogram(nanogram)
        answer.print_all()
        print('solved')
    except Exception as e:
        print(e)
        print('unsolvable')

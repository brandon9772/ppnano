from nanogram import Nanograms
from solver import Solver
from utilities import Utilities

filename = r'D:\python\nanogram\question\question1_5x5.txt'
nanogram = Nanograms(filename)
utilities = Utilities()
solver = Solver(utilities)

nanogram.print_all()
answer = solver.solve_nanogram(nanogram)
answer.print_all()

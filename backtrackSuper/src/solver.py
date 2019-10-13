class Solver:
    def __init__(self, utilities):
        self.utilities = utilities

    def solve_nanogram(self, nanogram):
        all_counter = [[0, -1, 0]]
        nanogram = self.utilities.clean_zero_max_size(nanogram)
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
            print('iteration')
            print(iteration)
            print('all_counter')
            print(all_counter)
            print(len(step_answer))
            print('-----')
            iteration += 1
            all_counter = self.utilities.get_next_step(nanogram, all_counter)
            print('next step')
            print(all_counter)
            print('------------------')
            step_answer = step_answer[:len(all_counter)]
            possible = True
            try:
                if all_counter[-1] == [3, 3, 0]:
                    step_answer[-1].print_all()
                right_cross_min = -1
                if all_counter[-1][2] > 0:
                    right_cross_min = all_counter[-2][1]
                next_nanogram = self.utilities.chain_fill(
                    step_answer[-1],
                    all_counter[-1],
                    right_cross_min
                )
                next_nanogram.print_all()
                possible = self.utilities.is_possible(next_nanogram)
            except Exception as e:
                print(e)
                possible = False
            if possible:
                if iteration > 15:
                    print('15')
                    pass
                next_nanogram.print_all()
                step_answer.append(next_nanogram)
                if (
                    all_counter[-1][0] == last_counter[0] and
                    all_counter[-1][2] == last_counter[1]
                ):
                    break
                next_counter = self.utilities.get_next_condition(
                    nanogram,
                    all_counter[-1]
                )
                all_counter.append(next_counter)
        return step_answer[-1]

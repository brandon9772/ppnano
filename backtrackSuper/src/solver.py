class Solver:
    def __init__(self, utilities):
        self.utilities = utilities

    def solve_nanogram(self, nanogram, max_iteration):
        all_counter = [[0, -1, 0]]
        nanogram = self.utilities.clean_zero_max_size(nanogram)
        step_answer = [nanogram]
        last_counter = [
            nanogram.row_size-1,
            len(nanogram.row_condition[-1]) - 1
        ]
        # loop
        next_nanogram = None
        iteration = 0
        for _ in range(max_iteration):
            iteration += 1
            # print('------------------')
            # print('iteration')
            # print(iteration)
            # print('all_counter')
            # print(all_counter)
            # print(len(step_answer))
            # print('-----')
            try:
                all_counter = self.utilities.get_next_step(
                    nanogram, all_counter)
            except Exception as e:
                print(iteration)
                raise e
            # print('next step')
            # print(all_counter)
            # print('------------------')
            step_answer = step_answer[:len(all_counter)]
            possible = True
            try:
                right_cross_min = -1
                if all_counter[-1][2] > 0:
                    right_cross_min = (
                        all_counter[-2][1]
                        + nanogram.row_condition[
                            all_counter[-2][0]
                        ][
                            all_counter[-2][2]
                        ][0]
                        - 1
                    )
                next_nanogram = self.utilities.chain_fill(
                    step_answer[-1],
                    all_counter[-1],
                    right_cross_min
                )
                possible = self.utilities.is_possible(next_nanogram)
            except Exception:
                # print(e)
                possible = False
            if possible:
                # next_nanogram.print_all()
                step_answer.append(next_nanogram)
                if (
                    all_counter[-1][0] == last_counter[0] and
                    all_counter[-1][2] == last_counter[1]
                ):
                    # next_nanogram.print_all()
                    # print('hererer')
                    break
                next_counter = self.utilities.get_next_condition(
                    nanogram,
                    all_counter[-1]
                )
                all_counter.append(next_counter)
        if iteration == max_iteration:
            print(len(step_answer))
            raise ValueError('out of iteration')
        return (step_answer[-1], iteration)

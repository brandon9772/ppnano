from pytest import param


class Data:
    def test_answer(self):
        variable = 'number'
        test_data = [
            param(
                '3',
                id='3'
            )
        ]

        return (variable, test_data)

from Nanograms import Nanograms
from Utilities import Utilities

filename = r'D:\python\nanogram\question\question1_5x5.txt'

nanogram = Nanograms(filename)
utilities = Utilities()

print(nanogram.row_condition)
print(nanogram.col_condition)
nanogram = utilities.update_to_must_fill_must_cross(nanogram)
nanogram.printAnsFillCross()
print('----------')
nanogram = utilities.update_from_must_fill(nanogram)
nanogram.printAnsFillCross()
print(list(nanogram.getAnswer()[1]))


# last_nanogram = copy.deepcopy(nanogram)
# last_nanogram.must_fill = 0
# print('while start')
# count = 0
# while(
#     (not nanogram.nanogram_equal(last_nanogram))
# ):
#     count += 1
#     print(count)
#     last_nanogram = nanogram
#     nanogram = utilities.update_to_must_fill_must_cross(nanogram)
#     nanogram = utilities.update_from_must_fill(nanogram)
# print('while end')

# nanogram.printAnsFillCross()
# answer = nanogram.getAnswer()
# if answer[0]:
#     print('solve')
#     nanogram.printAnsFillCross()
#     print('answer')
#     print(list(answer[1]))
# else:
#     print('not solve')
#     nanogram.printAnsFillCross()
#     print('answer')
#     print(list(answer[1]))

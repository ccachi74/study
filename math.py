'''
문제적남자 경기과학고 출제문제
a를 제곱한 후 b를 더했을 때 97540808
b를 제곱한 후 a를 더했을 때 29516500
a와 b를 구하라.
'''
from sympy import Symbol, solve

a = Symbol('a')
b = Symbol('b')

equation1 = a ** 2 + b - 97540808
equation2 = a + b ** 2 - 29516500

values = solve((equation1, equation2), dict=False)

for value in values:
    print(value)
import math


def midpoint(vec1: list[int], vec2: list[int]) -> tuple[float, float]:
    return (vec2[0] - vec1[0]) / 2 + vec1[0], (vec2[1] - vec1[1]) / 2 + vec1[1]


def calc_vec_distance(vec1: tuple[int, int], vec2: tuple[int, int]) -> float:
    return math.sqrt((vec1[0] - vec2[0])**2 + (vec1[1] - vec2[1])**2)


def first_n_digits(num, n):
    return num // 10 ** (int(math.log(num, 10)) - n + 1)

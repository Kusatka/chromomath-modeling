def ker(n):
    """Рекурсивная сумма цифр числа"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def model_ker_sum_squares(x, y):
    """Ker для суммы квадратов"""
    return ker(x * x + y * y)


def model_ker_sum_cubes(x, y):
    """Ker для суммы кубов"""
    return ker(x * x * x + y * y * y)

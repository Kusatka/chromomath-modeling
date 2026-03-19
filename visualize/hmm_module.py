def ker(n):
    """Рекурсивная сумма цифр числа (digital root). Обработка отрицательных значений."""
    if n < 0:
        return 0
    if n == 0:
        return 0
    result = n % 9
    return result if result != 0 else 9


def model_ker_sum_squares(x, y):
    """Ker для суммы квадратов"""
    return ker(x * x + y * y)


def model_ker_sum_cubes(x, y):
    """Ker для суммы кубов"""
    return ker(x * x * x + y * y * y)

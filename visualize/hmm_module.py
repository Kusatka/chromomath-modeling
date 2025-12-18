def ker(n):
    """
    Рекурсивная сумма цифр числа до однозначного результата (цифровой корень).
    Оптимизировано с использованием свойства mod 9.
    """
    if n < 0:
        return 0  # Обработка отрицательных значений
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
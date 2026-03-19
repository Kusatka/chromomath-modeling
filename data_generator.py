import os


def generate_cubes(count=2000):
    """Генерация списка кубов натуральных чисел от 1 до count."""
    if count < 1:
        raise ValueError("Count must be a positive integer")
    return [i**3 for i in range(1, count + 1)]


def save_cubes_to_file(cubes, file_path):
    """Сохранение списка кубов в файл."""
    with open(file_path, "w") as f:
        for cube in cubes:
            f.write(f"{cube}\n")


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "data.txt")
        cubes = generate_cubes(2000)
        save_cubes_to_file(cubes, file_path)
        print(f"Сгенерировано {len(cubes)} значений кубов")
        print(f"Файл сохранён в: {file_path}")
    except Exception as e:
        print(f"Ошибка генерации данных: {e}")

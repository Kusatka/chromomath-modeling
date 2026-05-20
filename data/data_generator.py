import os


def generate_cubes(start=1, end=3000):
    """
    Генерирует последовательность кубов n³ для n = start..end
    
    Args:
        start: начальное значение n (по умолчанию 1)
        end: конечное значение n (по умолчанию 3000)
    
    Returns:
        список кубических значений
    """
    return [i**3 for i in range(start, end + 1)]


def save_data(cubes, file_path):
    """
    Сохраняет данные в текстовый файл
    
    Args:
        cubes: список значений кубов
        file_path: путь к файлу для сохранения
    """
    try:
        with open(file_path, "w") as f:
            for cube in cubes:
                f.write(f"{cube}\n")
        return True, f"Сгенерировано {len(cubes)} значений кубов. Файл сохранён: {file_path}"
    except Exception as e:
        return False, f"Ошибка при сохранении: {e}"


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data.txt")
    
    cubes = generate_cubes(start=1, end=3000)
    success, message = save_data(cubes, file_path)
    
    print(message)
    if not success:
        print("Генерирование данных завершено с ошибкой!")
    else:
        print("✓ Данные успешно сгенерированы и сохранены")


if __name__ == "__main__":
    main()

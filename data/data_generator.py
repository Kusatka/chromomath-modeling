import os


def generate_cubes(count=1500):
    return [i**3 for i in range(1, count + 1)]


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")
cubes = generate_cubes()
with open(file_path, "w") as f:
    for cube in cubes:
        f.write(f"{cube}\n")
    print(f"Сгенерировано {len(cubes)} значений кубов")
    print(f"Файл сохранён в: {file_path}")

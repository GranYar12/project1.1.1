import os
import sys
import subprocess
import time
import shutil

def run_linpack_test(N, work_dir='.'):
    """
    Кроссплатформенный аналог scr1.sh.
    Запускает mylinpack для i от 2 до N с шагом 1,
    собирает время и сохраняет результат в results/time_<N>.txt.
    """
    exe_name = 'mylinpack_64.exe' if sys.platform.startswith('win') else 'mylinpack_64'
    exe_path = os.path.join(work_dir, exe_name)

    # 1. Проверить наличие исполняемого файла, при необходимости скомпилировать
    if not os.path.exists(exe_path):
        compile_mylinpack(work_dir, exe_name)

    # 2. Создать папку results, если её нет
    results_dir = os.path.join(work_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    # 3. Запустить тесты и собрать времена
    time_records = []
    for i in range(2, N + 1):
        start = time.perf_counter()
        try:
            subprocess.run([exe_path, str(i)], cwd=work_dir, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elapsed = time.perf_counter() - start
        except subprocess.CalledProcessError:
            # Если mylinpack упал, записываем 0.0, чтобы сохранить длину массива
            elapsed = 0.0
        time_records.append(elapsed)

    # 4. Сохранить времена в файл time_<N>.txt внутри results/
    output_file = os.path.join(results_dir, f'time_{N}.txt')
    with open(output_file, 'w') as f:
        for t in time_records:
            f.write(f'{t}\n')

    print(f"Тест 3, N={N}: результаты сохранены в {output_file}")

def compile_mylinpack(work_dir, exe_name):
    """Компилирует mylinpack.c, если возможно."""
    source = os.path.join(work_dir, 'mylinpack.c')
    if not os.path.exists(source):
        raise FileNotFoundError(f"Исходный файл {source} не найден.")

    if sys.platform.startswith('win'):
        # Пытаемся найти gcc (можно добавить пути, если нужно)
        gcc = shutil.which('gcc') or shutil.which('gcc.exe')
        if not gcc:
            raise RuntimeError(
                "Компилятор gcc не найден.\n"
                "Поместите заранее скомпилированный mylinpack_64.exe в папку теста или установите MinGW."
            )
        subprocess.run([gcc, source, '-o', exe_name], cwd=work_dir, check=True)
    else:
        subprocess.run(['gcc', source, '-o', exe_name], cwd=work_dir, check=True) #
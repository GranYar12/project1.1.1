import os
import subprocess
import time
import shutil
import sys

#huk
def run_linpack_test(N, work_dir='.'):
    """
    Кроссплатформенный аналог scr1.sh.
    Запускает mylinpack для всех i от 2 до N с шагом 1,
    замеряет время и вызывает paint_plot.py.
    """
    # 1. Определяем имя исполняемого файла в зависимости от ОС
    exe_name = 'mylinpack_64.exe' if sys.platform.startswith('win') else 'mylinpack_64'
    exe_path = os.path.join(work_dir, exe_name)

    # 2. Если бинарника нет, компилируем
    if not os.path.exists(exe_path):
        compile_mylinpack(work_dir, exe_name)

    # 3. Создаём временные папки (если они ещё не созданы)
    tmp_dir = os.path.join(work_dir, 'tmp')
    var_dir = os.path.join(work_dir, 'var')
    results_dir = os.path.join(work_dir, 'results')
    pictures_dir = os.path.join(work_dir, 'pictures')
    for d in [tmp_dir, var_dir, results_dir, pictures_dir]:
        os.makedirs(d, exist_ok=True)

    # 4. Запускаем тесты и собираем время
    number_of_variables = []
    real_times = []

    STEPX = 1  # как в исходном скрипте
    for i in range(2, N + STEPX, STEPX):
        # Засекаем время
        start = time.perf_counter()
        try:
            subprocess.run([exe_path, str(i)], cwd=work_dir, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка выполнения mylinpack для i={i}: {e}")
            # Можно продолжить или прервать; для совместимости продолжим
        elapsed = time.perf_counter() - start

        number_of_variables.append(i)
        real_times.append(elapsed)

    # 5. Сохраняем результаты в файлы (как этого ожидает paint_plot.py)
    var_file = os.path.join(var_dir, 'number_of_variables')
    time_file = os.path.join(var_dir, 'real_time')

    with open(var_file, 'w') as f:
        f.write('\n'.join(str(x) for x in number_of_variables))
    with open(time_file, 'w') as f:
        f.write('\n'.join(f'{t:.6f}' for t in real_times))

    # 6. Вызываем paint_plot.py
    paint_script = os.path.join(work_dir, 'paint_plot.py')
    if os.path.exists(paint_script):
        subprocess.run([sys.executable, paint_script, time_file, var_file],
                       cwd=work_dir, check=True)
    else:
        print("Предупреждение: paint_plot.py не найден, графики не построены.")

    # 7. Удаляем временные папки
    shutil.rmtree(tmp_dir, ignore_errors=True)
    shutil.rmtree(var_dir, ignore_errors=True)

def compile_mylinpack(work_dir, exe_name):
    """Пытается скомпилировать mylinpack.c с помощью gcc."""
    source = os.path.join(work_dir, 'mylinpack.c')
    if not os.path.exists(source):
        raise FileNotFoundError(f"Исходный файл {source} не найден. Невозможно скомпилировать mylinpack.")

    # Проверяем наличие gcc
    gcc_cmd = 'gcc'
    if sys.platform.startswith('win'):
        # В Windows может быть 'gcc.exe' из MinGW
        if shutil.which('gcc') is None and shutil.which('gcc.exe') is None:
            raise RuntimeError(
                "Компилятор gcc не найден. Установите MinGW-w64 или скомпилируйте mylinpack_64.exe "
                "заранее и поместите его в папку теста."
            )
    try:
        subprocess.run([gcc_cmd, source, '-o', exe_name], cwd=work_dir, check=True)
        print(f"{exe_name} успешно скомпилирован.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Не удалось скомпилировать mylinpack: {e}")
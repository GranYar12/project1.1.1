import os
import sys
import shutil
import subprocess
from predict_1200 import main_1200
from linpack_runner import run_linpack_test  # наш новый модуль

def main(N):
    N_list = get_from_manager(N)
    for i in N_list:
        # Вместо старого условия теперь всегда запускаем кроссплатформенный вариант
        run_linpack_test(i, work_dir='.')  # work_dir — папка, где лежит mylinpack.c и paint_plot.py

    if 1000 in N_list:
        main_1200(N_list)

def get_from_manager(N):
    ind = ['25', '50', '100', '150', '200', '300', '500', '1000', '1200']
    result_N = []
    for i in ind:
        if i in N:
            result_N.append(int(i))
    return result_N

if __name__ == '__main__':
    N = sys.argv[1]
    print('in new_scr=', N[0])
    main(N)

    # Копирование результатов (без изменений)
    src = 'results'
    dst = os.path.abspath(os.path.join('..', '..', 'visual', '3_test'))
    if os.path.exists(src):
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    # if os.path.exists('mylinpack_64'):
    #     os.remove('mylinpack_64')
    #  для Windows не забываем удалить .exe, если был
    # if os.path.exists('mylinpack_64.exe'):
    #     os.remove('mylinpack_64.exe')                                                         #kkлл
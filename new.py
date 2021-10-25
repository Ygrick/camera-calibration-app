import multiprocessing
import time


def heavy(n, i, proc):
    for x in range(1, n):
        for y in range(1, n):
            x ** y
    print(f"Цикл № {i} ядро {proc}")


def sequential(calc, proc):
    print(f"Запускаем поток № {proc}")
    for i in range(calc):
        heavy(500, i, proc)
    print(f"{calc} циклов вычислений закончены. Процессор № {proc}")


def processesed(procs, calc):
    # procs - количество ядер
    # calc - количество операций на ядро

    processes = []

    # делим вычисления на количество ядер
    for proc in range(procs):
        p = multiprocessing.Process(target=sequential, args=(calc, proc))
        processes.append(p)
        p.start()

    # Ждем, пока все ядра 
    # завершат свою работу.
    for p in processes:
        p.join()


if __name__ == "__main__":
    start = time.time()
    # узнаем количество ядер у процессора
    n_proc = multiprocessing.cpu_count()
    # вычисляем сколько циклов вычислений будет приходится
    # на 1 ядро, что бы в сумме получилось 80 или чуть больше
    calc = 80 // n_proc + 1
    processesed(n_proc, calc)
    end = time.time()
    print(f"Всего {n_proc} ядер в процессоре")
    print(f"На каждом ядре произведено {calc} циклов вычислений")
    print(f"Итого {n_proc * calc} циклов за: ", end - start)

# Весь вывод показывать не будем
# ...
# ...
# ...
# Всего 6 ядер в процессоре
# На каждом ядре произведено 14 циклов вычислений
# Итого 84 циклов вычислений за:  5.0251686573028564
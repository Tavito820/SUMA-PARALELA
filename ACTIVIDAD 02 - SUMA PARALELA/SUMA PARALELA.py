import multiprocessing
import random
import time

# Tamaño de los arrays
N = 100000

# Número de procesos
NUM_PROCESOS = multiprocessing.cpu_count()

# Función para sumar elementos en paralelo
def worker(start, end, a, b, c):
    for i in range(start, end):
        c[i] = a[i] + b[i]

# Función para suma ordinaria
def suma_ordinaria(a, b):
    c = [0] * len(a)
    for i in range(len(a)):
        c[i] = a[i] + b[i]
    return c

if __name__ == "__main__":
    # Generar arrays aleatorios
    a = [random.randint(1, 100) for _ in range(N)]
    b = [random.randint(1, 100) for _ in range(N)]

    # Suma ordinaria
    start_time = time.time()
    c_ordinaria = suma_ordinaria(a, b)
    tiempo_ordinaria = time.time() - start_time
    print(f"Tiempo de suma ordinaria: {tiempo_ordinaria:.6f} segundos")

    # Suma paralela
    c_paralelo = multiprocessing.Array('i', N)  # Array compartido
    
    start_time = time.time()
    
    processes = []
    chunk_size = N // NUM_PROCESOS
    for i in range(NUM_PROCESOS):
        start = i * chunk_size
        end = N if i == NUM_PROCESOS - 1 else (i + 1) * chunk_size
        process = multiprocessing.Process(target=worker, args=(start, end, a, b, c_paralelo))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    tiempo_paralelo = time.time() - start_time
    print(f"Tiempo de suma paralela: {tiempo_paralelo:.6f} segundos")

    # Para verificar la precisión, puedes comparar los primeros elementos de ambos resultados:
    print(f"Primeros 10 elementos de suma ordinaria: {c_ordinaria[:10]}")
    print(f"Primeros 10 elementos de suma paralela: {list(c_paralelo[:10])}")


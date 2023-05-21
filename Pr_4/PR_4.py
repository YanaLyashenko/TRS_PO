import random
import threading
import queue
import time


arr_row = [random.randint(1, 100) for _ in range(1000)] # генеруємо випадковий масив розміром 1000 з чисел від 1 до 100

arr_row = sorted(arr_row) # сортуємо масив за зростанням

def find_mode(q, start, end): # функція, що знаходить моду
    mode = None
    max_count = 0
    
    for i in range(start, end):
        count = arr_row.count(arr_row[i]) # рахуємо кількість входжень елементу в масив
        if count > max_count:
            max_count = count # знаходимо найбільшу кількість входжень
            mode = arr_row[i] # та саме число, яке входить цю кількість разів
    
    q.put((mode, max_count)) # поміщаємо знайдену моду в чергу q разом з кількістю входжень

q = queue.Queue()
threads = []

for i in range(4):
    start = i * len(arr_row) // 4 # обчислюємо початковий і кінцевий індекс для потоку
    end = (i + 1) * len(arr_row) // 4
    t = threading.Thread(target=find_mode, args=(q, start, end)) # створюємо потік, якому передаємо чергу та інтервал обчислень
    threads.append(t) # додаємо потік до списку потоків

start_time = time.time() # запам'ятовуємо час початку виконання програми

for t in threads:
    t.start() # запускаємо кожен потік

for t in threads:
    t.join() # очікуємо завершення кожного потоку

end_time = time.time() # запам'ятовуємо час завершення виконання програми

mode_counts = {}
while not q.empty():
    mode, count = q.get() # отримуємо моду та кількість входжень з черги
    if mode in mode_counts:
        mode_counts[mode] += count # додаємо кількість входжень до моди, якщо вона вже зустрічалась
    else:
        mode_counts[mode] = count # додаємо нову моду до словника mode_counts

mode = max(mode_counts, key=mode_counts.get) # знаходимо моду за значенням кількості входжень

print("Варіаційний ряд:", arr_row)
print("Мода:", mode)
print("Час виконання програми: {0:.5f} секунд".format(end_time - start_time))
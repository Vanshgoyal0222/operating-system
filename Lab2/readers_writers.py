import threading
import time

readers = int(input("Enter number of readers: "))
writers = int(input("Enter number of writers: "))
iterations = int(input("Enter number of iterations: "))

read_count = 0
data = 0

read_count_lock = threading.Lock()
write_lock = threading.Lock()


def reader(reader_id):
    global read_count

    for _ in range(iterations):
        with read_count_lock:
            read_count += 1

            if read_count == 1:
                write_lock.acquire()

        print("Reader", reader_id, "is reading data:", data)
        time.sleep(0.1)

        with read_count_lock:
            read_count -= 1

            if read_count == 0:
                write_lock.release()

        time.sleep(0.1)


def writer(writer_id):
    global data

    for _ in range(iterations):
        with write_lock:
            data += 1
            print("Writer", writer_id, "updated data to:", data)
            time.sleep(0.15)

        time.sleep(0.1)


threads = []

for i in range(1, readers + 1):
    t = threading.Thread(target=reader, args=(i,))
    threads.append(t)
    t.start()

for i in range(1, writers + 1):
    t = threading.Thread(target=writer, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nReaders-Writers completed successfully.")
print("Final data:", data)
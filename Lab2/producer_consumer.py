import threading
import time

buffer_size = int(input("Enter buffer size: "))
items = int(input("Enter number of items: "))

buffer = []
mutex = threading.Lock()
empty = threading.Semaphore(buffer_size)
full = threading.Semaphore(0)


def producer():
    for i in range(1, items + 1):
        empty.acquire()

        with mutex:
            buffer.append(i)
            print("Producer produced:", i)
            print("Buffer:", buffer)

        full.release()
        time.sleep(0.1)


def consumer():
    for _ in range(items):
        full.acquire()

        with mutex:
            item = buffer.pop(0)
            print("Consumer consumed:", item)
            print("Buffer:", buffer)

        empty.release()
        time.sleep(0.15)


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print("\nProducer-Consumer completed successfully.")
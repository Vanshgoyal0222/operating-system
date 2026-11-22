import threading
import time


def unprotected(num_threads, increments):
    counter = [0]

    def increment():
        for _ in range(increments):
            value = counter[0]
            time.sleep(0)
            counter[0] = value + 1

    threads = []
    start = time.perf_counter()

    for _ in range(num_threads):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()

    return counter[0], end - start


def lock_version(num_threads, increments):
    counter = [0]
    lock = threading.Lock()

    def increment():
        for _ in range(increments):
            with lock:
                counter[0] += 1

    threads = []
    start = time.perf_counter()

    for _ in range(num_threads):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()

    return counter[0], end - start


def semaphore_version(num_threads, increments):
    counter = [0]
    semaphore = threading.Semaphore(1)

    def increment():
        for _ in range(increments):
            semaphore.acquire()
            counter[0] += 1
            semaphore.release()

    threads = []
    start = time.perf_counter()

    for _ in range(num_threads):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()

    return counter[0], end - start


print("=" * 55)
print("RACE CONDITION, LOCK AND SEMAPHORE")
print("=" * 55)

num_threads = int(input("Enter number of threads: "))
increments = int(input("Enter increments per thread: "))

expected = num_threads * increments

print("\nExpected Result:", expected)

print("\n--- Unprotected Version ---")
result, execution_time = unprotected(num_threads, increments)
print("Actual Result:", result)
print("Execution Time:", execution_time, "seconds")
print("Correct:", result == expected)

print("\n--- Lock Version ---")
result, execution_time = lock_version(num_threads, increments)
print("Actual Result:", result)
print("Execution Time:", execution_time, "seconds")
print("Correct:", result == expected)

print("\n--- Semaphore Version ---")
result, execution_time = semaphore_version(num_threads, increments)
print("Actual Result:", result)
print("Execution Time:", execution_time, "seconds")
print("Correct:", result == expected)

print("\n" + "=" * 55)
print("Assignment Completed")
print("=" * 55)
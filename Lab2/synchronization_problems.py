"""
Classical Synchronization Problems - Operating Systems Lab Assignment

Implements:
1. Producer-Consumer with a finite circular buffer and semaphores
2. Readers-Writers with protected reader count and exclusive writer access
3. Dining Philosophers with controlled shared-resource access
4. Deadlock prevention via semaphores, a waiter, and resource ordering
5. Finite iterations so all threads terminate
6. Displays shared-resource states and thread operations

Run: python synchronization_problems.py
"""

import threading
import time
from collections import deque

# Small delays make thread interleaving easier to observe in the terminal.
DELAY = 0.05


def producer_consumer():
    print("\n" + "=" * 58)
    print("1. PRODUCER-CONSUMER: FINITE CIRCULAR BUFFER")
    print("=" * 58)

    capacity = 3
    total_items = 8
    buffer = [None] * capacity
    in_index = 0
    out_index = 0
    count = 0

    mutex = threading.Lock()
    empty = threading.Semaphore(capacity)
    full = threading.Semaphore(0)

    def producer():
        nonlocal in_index, count
        for item in range(1, total_items + 1):
            empty.acquire()
            with mutex:
                buffer[in_index] = item
                in_index = (in_index + 1) % capacity
                count += 1
                print(f"Producer: added {item} | Buffer: {buffer} | Items: {count}/{capacity}")
            full.release()
            time.sleep(DELAY)

    def consumer():
        nonlocal out_index, count
        for _ in range(total_items):
            full.acquire()
            with mutex:
                item = buffer[out_index]
                buffer[out_index] = None
                out_index = (out_index + 1) % capacity
                count -= 1
                print(f"Consumer: removed {item} | Buffer: {buffer} | Items: {count}/{capacity}")
            empty.release()
            time.sleep(DELAY)

    p = threading.Thread(target=producer, name="Producer")
    c = threading.Thread(target=consumer, name="Consumer")
    p.start()
    c.start()
    p.join()
    c.join()
    print("Producer-Consumer finished: all items were produced and consumed.")


def readers_writers():
    print("\n" + "=" * 58)
    print("2. READERS-WRITERS: SHARED READ, EXCLUSIVE WRITE")
    print("=" * 58)

    reader_count = 0
    reader_count_lock = threading.Lock()
    room_empty = threading.Semaphore(1)
    shared_data = {"value": 0}

    def reader(reader_id):
        nonlocal reader_count
        with reader_count_lock:
            reader_count += 1
            if reader_count == 1:
                room_empty.acquire()
            print(f"Reader {reader_id} starts reading | Active readers: {reader_count}")

        time.sleep(DELAY)
        value = shared_data["value"]
        print(f"Reader {reader_id} read value: {value}")

        with reader_count_lock:
            reader_count -= 1
            print(f"Reader {reader_id} finished | Active readers: {reader_count}")
            if reader_count == 0:
                room_empty.release()

    def writer(writer_id):
        with room_empty:
            old_value = shared_data["value"]
            shared_data["value"] = old_value + 1
            print(f"Writer {writer_id} exclusively changed value: {old_value} -> {shared_data['value']}")
            time.sleep(DELAY)

    threads = [
        threading.Thread(target=reader, args=(1,)),
        threading.Thread(target=reader, args=(2,)),
        threading.Thread(target=writer, args=(1,)),
        threading.Thread(target=reader, args=(3,)),
        threading.Thread(target=writer, args=(2,)),
    ]
    for thread in threads:
        thread.start()
        time.sleep(0.01)
    for thread in threads:
        thread.join()

    print(f"Readers-Writers finished | Final shared value: {shared_data['value']}")
    print("Readers may share access; writers hold exclusive access.")


def dining_philosophers():
    print("\n" + "=" * 58)
    print("3. DINING PHILOSOPHERS: CONTROLLED RESOURCE ACCESS")
    print("=" * 58)

    number = 5
    meals_each = 2
    forks = [threading.Lock() for _ in range(number)]
    # A waiter permits at most N-1 philosophers to try to pick up forks.
    waiter = threading.Semaphore(number - 1)

    def philosopher(pid):
        left = pid
        right = (pid + 1) % number
        for meal in range(1, meals_each + 1):
            print(f"Philosopher {pid} is thinking.")
            time.sleep(DELAY)
            with waiter:
                # Fixed ordering of fork indexes prevents circular wait.
                first, second = sorted((left, right))
                with forks[first]:
                    print(f"Philosopher {pid} picked up fork {first}.")
                    with forks[second]:
                        print(f"Philosopher {pid} picked up fork {second}.")
                        print(f"Philosopher {pid} is eating meal {meal}.")
                        time.sleep(DELAY)
                print(f"Philosopher {pid} put down both forks.")

    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(number)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Dining Philosophers finished: every philosopher ate twice.")
    print("Deadlock is prevented using a waiter and consistent fork ordering.")


def theory_summary():
    print("\n" + "=" * 58)
    print("4. DEADLOCK, STARVATION, FAIRNESS AND CORRECTNESS")
    print("=" * 58)
    print("Deadlock: threads wait forever for resources held by one another.")
    print("Starvation: a thread waits indefinitely while others keep progressing.")
    print("Fairness: threads should get reasonable opportunities to access resources.")
    print("Correctness: shared data stays consistent and synchronization rules are obeyed.")
    print("\nMechanisms used:")
    print("- Producer-Consumer: mutex + empty/full semaphores + circular buffer.")
    print("- Readers-Writers: protected reader count + exclusive writer semaphore.")
    print("- Dining Philosophers: waiter semaphore + globally ordered fork locks.")
    print("- Finite loops and thread.join() ensure the demonstrations terminate.")


def main():
    print("#" * 58)
    print(" CLASSICAL SYNCHRONIZATION PROBLEMS")
    print("#" * 58)
    print("1. Producer-Consumer")
    print("2. Readers-Writers")
    print("3. Dining Philosophers")
    print("4. Theory summary")
    print("5. Run all demonstrations")
    print("0. Exit")

    while True:
        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            producer_consumer()
        elif choice == "2":
            readers_writers()
        elif choice == "3":
            dining_philosophers()
        elif choice == "4":
            theory_summary()
        elif choice == "5":
            producer_consumer()
            readers_writers()
            dining_philosophers()
            theory_summary()
        elif choice == "0":
            print("Exiting. All demonstrations completed safely.")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, 4, 5, or 0.")


if __name__ == "__main__":
    main()
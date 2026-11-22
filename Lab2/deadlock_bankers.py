"""
Deadlock Handling and Banker's Algorithm
Operating Systems Lab Assignment

Covers:
1. Controlled circular-wait scenario (uses timeouts so it cannot hang forever)
2. Deadlock prevention using resource ordering
3. Allocation, Maximum, Available input
4. Need matrix calculation
5. Banker's safety algorithm and safe sequence
6. Deadlock detection
7. Recovery by releasing resources / terminating a process
"""

import threading
import time


def print_conditions():
    print("\nFour necessary conditions for deadlock:")
    print("1. Mutual exclusion: a resource can be held by only one process at a time.")
    print("2. Hold and wait: a process holds one resource while waiting for another.")
    print("3. No preemption: resources cannot be forcibly taken away.")
    print("4. Circular wait: processes form a cycle, each waiting for a resource held by the next.")
    print("\nPrevention method used here: resource ordering.")
    print("Every process must acquire resources in increasing ID/order, preventing circular wait.")


def controlled_circular_wait():
    """Illustrate circular wait with timeouts to avoid permanent blocking."""
    print("\n--- Controlled Circular-Wait Demonstration ---")
    first = threading.Lock()
    second = threading.Lock()
    barrier = threading.Barrier(2)

    def process(name, first_lock, second_lock):
        print(f"{name}: acquiring its first resource...")
        first_lock.acquire()
        print(f"{name}: acquired first resource.")
        try:
            barrier.wait(timeout=2)
            print(f"{name}: requesting its second resource (timeout: 2 seconds)...")
            got_second = second_lock.acquire(timeout=2)
            if got_second:
                print(f"{name}: acquired second resource; no deadlock this run.")
                second_lock.release()
            else:
                print(f"{name}: timed out waiting. Deadlock risk detected; releasing first resource.")
        except threading.BrokenBarrierError:
            print(f"{name}: synchronization barrier timed out.")
        finally:
            first_lock.release()
            print(f"{name}: released first resource.")

    t1 = threading.Thread(target=process, args=("Process P1", first, second))
    t2 = threading.Thread(target=process, args=("Process P2", second, first))
    t1.start()
    t2.start()
    t1.join(timeout=6)
    t2.join(timeout=6)
    print("Result: both threads finish because lock acquisition has a timeout.")
    print_conditions()


def prevention_resource_ordering():
    """Demonstrate prevention by always acquiring locks in the same order."""
    print("\n--- Deadlock Prevention: Resource Ordering ---")
    resource_1 = threading.Lock()
    resource_2 = threading.Lock()

    def worker(name):
        # Both workers acquire Resource 1 before Resource 2.
        with resource_1:
            print(f"{name}: acquired Resource 1.")
            time.sleep(0.2)
            with resource_2:
                print(f"{name}: acquired Resource 2.")
                time.sleep(0.2)
        print(f"{name}: released both resources.")

    t1 = threading.Thread(target=worker, args=("Process P1",))
    t2 = threading.Thread(target=worker, args=("Process P2",))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Result: consistent resource ordering prevents circular wait.")


def read_matrix(prompt, rows, cols):
    print(prompt)
    matrix = []
    for i in range(rows):
        while True:
            try:
                values = list(map(int, input(f"Row {i} (enter {cols} integers separated by spaces): ").split()))
                if len(values) != cols or any(v < 0 for v in values):
                    print(f"Please enter exactly {cols} non-negative integers.")
                    continue
                matrix.append(values)
                break
            except ValueError:
                print("Invalid input. Enter integers only.")
    return matrix


def read_vector(prompt, size):
    while True:
        try:
            values = list(map(int, input(f"{prompt} ({size} integers separated by spaces): ").split()))
            if len(values) != size or any(v < 0 for v in values):
                print(f"Please enter exactly {size} non-negative integers.")
                continue
            return values
        except ValueError:
            print("Invalid input. Enter integers only.")


def banker_safety(allocation, maximum, available):
    n = len(allocation)
    m = len(available)
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    work = available[:]
    finish = [False] * n
    safe_sequence = []

    print("\nNeed Matrix = Maximum - Allocation:")
    for i, row in enumerate(need):
        print(f"P{i}: {row}")

    print(f"\nInitial Work/Available: {work}")
    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                print(f"P{i} can finish because Need {need[i]} <= Work {work}.")
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                safe_sequence.append(f"P{i}")
                print(f"P{i} finishes; releases allocation. New Work: {work}")
                found = True
        if not found:
            break

    if all(finish):
        print("\nSAFE STATE")
        print("Safe sequence:", " -> ".join(safe_sequence))
    else:
        unfinished = [f"P{i}" for i, done in enumerate(finish) if not done]
        print("\nUNSAFE STATE: no safe sequence exists for the supplied data.")
        print("Processes that could not be completed:", ", ".join(unfinished))
    return need, all(finish), safe_sequence


def banker_menu():
    print("\n--- Banker's Safety Algorithm ---")
    while True:
        try:
            n = int(input("Number of processes: "))
            m = int(input("Number of resource types: "))
            if n <= 0 or m <= 0:
                print("Both values must be positive.")
                continue
            break
        except ValueError:
            print("Enter whole numbers.")

    allocation = read_matrix("Enter Allocation matrix:", n, m)
    maximum = read_matrix("Enter Maximum matrix:", n, m)
    available = read_vector("Enter Available vector", m)

    invalid = any(allocation[i][j] > maximum[i][j] for i in range(n) for j in range(m))
    if invalid:
        print("Error: Allocation cannot be greater than Maximum. Please run again.")
        return
    banker_safety(allocation, maximum, available)


def deadlock_detection():
    """Detection algorithm using Allocation, Request and Available."""
    print("\n--- Deadlock Detection Algorithm ---")
    while True:
        try:
            n = int(input("Number of processes: "))
            m = int(input("Number of resource types: "))
            if n <= 0 or m <= 0:
                print("Both values must be positive.")
                continue
            break
        except ValueError:
            print("Enter whole numbers.")

    allocation = read_matrix("Enter current Allocation matrix:", n, m)
    request = read_matrix("Enter current outstanding Request matrix:", n, m)
    available = read_vector("Enter currently Available vector", m)

    work = available[:]
    finish = [all(allocation[i][j] == 0 for j in range(m)) for i in range(n)]
    # Processes holding no resources can be considered able to finish.
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if not finish[i] and all(request[i][j] <= work[j] for j in range(m)):
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                changed = True
                print(f"P{i} can complete and release resources. Work becomes {work}.")

    stuck = [f"P{i}" for i, done in enumerate(finish) if not done]
    if stuck:
        print("Possible deadlock detected. Processes unable to finish:", ", ".join(stuck))
    else:
        print("No deadlock detected: all processes can finish.")


def recovery_demo():
    print("\n--- Controlled Deadlock Recovery ---")
    print("Example: P0 holds one resource and waits for another; P1 holds the needed resource.")
    print("Recovery options:")
    print("1. Release a resource voluntarily, if safe and permitted.")
    print("2. Terminate one process to release its resources.")
    choice = input("Choose recovery action (1 = release resource, 2 = terminate process): ").strip()
    if choice == "1":
        print("P1 releases Resource R1. The waiting process can retry and continue.")
        print("Recovery complete: resource released; no process was terminated.")
    elif choice == "2":
        process = input("Enter process to terminate (e.g., P1): ").strip() or "P1"
        print(f"{process} is terminated; its allocated resources are returned to the available pool.")
        print("Recovery complete: remaining processes can be scheduled again.")
    else:
        print("Invalid choice. No recovery action was performed.")


def main():
    while True:
        print("\n" + "=" * 52)
        print(" DEADLOCK HANDLING AND BANKER'S ALGORITHM")
        print("=" * 52)
        print("1. Controlled circular-wait scenario")
        print("2. Deadlock prevention using resource ordering")
        print("3. Banker's Algorithm (Allocation, Maximum, Available, Need, safe sequence)")
        print("4. Deadlock detection")
        print("5. Deadlock recovery (resource release / process termination)")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            controlled_circular_wait()
        elif choice == "2":
            prevention_resource_ordering()
        elif choice == "3":
            banker_menu()
        elif choice == "4":
            deadlock_detection()
        elif choice == "5":
            recovery_demo()
        elif choice == "6":
            print("Exiting program. All done!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
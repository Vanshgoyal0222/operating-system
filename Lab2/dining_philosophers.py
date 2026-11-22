import threading
import time

philosophers = int(input("Enter number of philosophers: "))
iterations = int(input("Enter number of eating rounds: "))

forks = [threading.Lock() for _ in range(philosophers)]


def philosopher(philosopher_id):
    left = philosopher_id
    right = (philosopher_id + 1) % philosophers

    first = min(left, right)
    second = max(left, right)

    for _ in range(iterations):
        print("Philosopher", philosopher_id, "is thinking.")
        time.sleep(0.1)

        forks[first].acquire()
        print("Philosopher", philosopher_id, "picked fork", first)

        forks[second].acquire()
        print("Philosopher", philosopher_id, "picked fork", second)

        print("Philosopher", philosopher_id, "is eating.")
        time.sleep(0.2)

        forks[second].release()
        forks[first].release()

        print("Philosopher", philosopher_id, "released both forks.")


threads = []

for i in range(philosophers):
    t = threading.Thread(target=philosopher, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nDining Philosophers completed successfully.")
print("No permanent deadlock occurred.")
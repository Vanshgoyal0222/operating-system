def first_fit(blocks, processes):
    remaining = blocks.copy()
    allocation = [-1] * len(processes)

    for i, process in enumerate(processes):
        for j in range(len(remaining)):
            if remaining[j] >= process:
                allocation[i] = j
                remaining[j] -= process
                break

    return allocation, remaining


def best_fit(blocks, processes):
    remaining = blocks.copy()
    allocation = [-1] * len(processes)

    for i, process in enumerate(processes):
        suitable = [j for j in range(len(remaining))
                    if remaining[j] >= process]

        if suitable:
            index = min(suitable, key=lambda j: remaining[j])
            allocation[i] = index
            remaining[index] -= process

    return allocation, remaining


def worst_fit(blocks, processes):
    remaining = blocks.copy()
    allocation = [-1] * len(processes)

    for i, process in enumerate(processes):
        suitable = [j for j in range(len(remaining))
                    if remaining[j] >= process]

        if suitable:
            index = max(suitable, key=lambda j: remaining[j])
            allocation[i] = index
            remaining[index] -= process

    return allocation, remaining


def display_allocation(name, blocks, processes, allocation, remaining):
    print(f"\n========== {name} ==========")

    for i, process in enumerate(processes):
        if allocation[i] != -1:
            print(f"Process P{i + 1} ({process}) -> Block "
                  f"B{allocation[i] + 1}")
        else:
            print(f"Process P{i + 1} ({process}) -> Not Allocated")

    print("\nRemaining Block Sizes:")

    for i, size in enumerate(remaining):
        print(f"Block B{i + 1}: {size}")

    allocated = sum(1 for x in allocation if x != -1)
    unallocated = len(processes) - allocated

    print("\nAllocated Processes:", allocated)
    print("Unallocated Processes:", unallocated)


def address_translation():
    print("\n========== ADDRESS TRANSLATION ==========")

    base = int(input("Enter base address: "))
    limit = int(input("Enter limit: "))
    logical = int(input("Enter logical address: "))

    print("\nBase Address:", base)
    print("Limit:", limit)
    print("Logical Address:", logical)

    if base < 0 or limit <= 0 or logical < 0:
        print("Invalid address values.")
        return

    if logical >= limit:
        print("Error: Logical address exceeds limit.")
    else:
        physical = base + logical
        print("Formula: Physical Address = Base + Logical Address")
        print("Calculation:", base, "+", logical)
        print("Physical Address:", physical)


def swapping():
    print("\n========== SWAPPING ==========")

    blocks = list(map(int, input("Enter memory block sizes: ").split()))
    processes = list(map(int, input("Enter process sizes: ").split()))

    allocation, remaining = first_fit(blocks, processes)

    print("\n--- Memory Before Swapping ---")
    display_allocation("FIRST FIT", blocks, processes, allocation, remaining)

    outgoing = int(input("\nEnter outgoing process number (1-based): ")) - 1

    if outgoing < 0 or outgoing >= len(processes):
        print("Invalid process number.")
        return

    if allocation[outgoing] == -1:
        print("Process is not allocated. Cannot swap it out.")
        return

    block_index = allocation[outgoing]

    print(f"\nReleasing Process P{outgoing + 1} from Block B{block_index + 1}")

    remaining[block_index] += processes[outgoing]
    allocation[outgoing] = -1

    incoming_size = int(input("Enter incoming process size: "))

    if incoming_size <= 0:
        print("Invalid process size.")
        return

    print("\n--- Allocation of Incoming Process ---")

    allocated_block = -1

    for i in range(len(remaining)):
        if remaining[i] >= incoming_size:
            allocated_block = i
            remaining[i] -= incoming_size
            break

    if allocated_block != -1:
        print(f"Incoming Process ({incoming_size}) allocated to "
              f"Block B{allocated_block + 1}")
    else:
        print("Incoming process could not be allocated.")

    print("\n--- Memory After Swapping ---")

    for i, size in enumerate(remaining):
        print(f"Block B{i + 1}: Remaining Size = {size}")


def main():
    blocks = list(map(int, input("Enter memory block sizes: ").split()))
    processes = list(map(int, input("Enter process sizes: ").split()))

    if not blocks or not processes or any(x <= 0 for x in blocks + processes):
        print("Enter valid positive memory and process sizes.")
        return

    print("\nMemory Blocks:", blocks)
    print("Process Sizes:", processes)

    a1, r1 = first_fit(blocks, processes)
    a2, r2 = best_fit(blocks, processes)
    a3, r3 = worst_fit(blocks, processes)

    display_allocation("FIRST FIT", blocks, processes, a1, r1)
    display_allocation("BEST FIT", blocks, processes, a2, r2)
    display_allocation("WORST FIT", blocks, processes, a3, r3)

    address_translation()
    swapping()


main()
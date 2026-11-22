def fifo(pages, frame_count):
    frames = []
    hits = 0
    faults = 0
    pointer = 0

    print("\n--- FIFO ---")

    for page in pages:
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            faults += 1
            status = "Page Fault"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames[pointer] = page
                pointer = (pointer + 1) % frame_count

        print(f"Page: {page} | {status} | Frames: {frames}")

    return hits, faults


def lru(pages, frame_count):
    frames = []
    hits = 0
    faults = 0

    print("\n--- LRU ---")

    for page in pages:
        if page in frames:
            hits += 1
            status = "Hit"
            frames.remove(page)
            frames.append(page)
        else:
            faults += 1
            status = "Page Fault"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)

        print(f"Page: {page} | {status} | Frames: {frames}")

    return hits, faults


def optimal(pages, frame_count):
    frames = []
    hits = 0
    faults = 0

    print("\n--- Optimal ---")

    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            faults += 1
            status = "Page Fault"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                future = pages[i + 1:]
                distances = []

                for frame in frames:
                    if frame in future:
                        distances.append(future.index(frame))
                    else:
                        distances.append(float("inf"))

                victim = distances.index(max(distances))
                frames[victim] = page

        print(f"Page: {page} | {status} | Frames: {frames}")

    return hits, faults


def display_result(name, result, total):
    hits, faults = result

    hit_ratio = hits / total
    fault_ratio = faults / total

    print(f"\n{name} Results")
    print("Total References:", total)
    print("Total Hits:", hits)
    print("Total Page Faults:", faults)
    print("Hit Ratio:", round(hit_ratio, 2))
    print("Fault Ratio:", round(fault_ratio, 2))
    print("Hit Percentage:", round(hit_ratio * 100, 2), "%")
    print("Fault Percentage:", round(fault_ratio * 100, 2), "%")

    return faults


def main():
    while True:
        pages = list(map(int, input("\nEnter page reference string: ").split()))
        frame_count = int(input("Enter number of frames: "))

        if frame_count <= 0 or not pages:
            print("Invalid input.")
            continue

        total = len(pages)

        f = fifo(pages, frame_count)
        l = lru(pages, frame_count)
        o = optimal(pages, frame_count)

        fifo_faults = display_result("FIFO", f, total)
        lru_faults = display_result("LRU", l, total)
        optimal_faults = display_result("Optimal", o, total)

        print("\n--- Algorithm Comparison ---")
        print("FIFO Page Faults:", fifo_faults)
        print("LRU Page Faults:", lru_faults)
        print("Optimal Page Faults:", optimal_faults)

        print("\nBest Algorithm:", min(
            [("FIFO", fifo_faults),
             ("LRU", lru_faults),
             ("Optimal", optimal_faults)],
            key=lambda x: x[1]
        )[0])

        if max(f[1], l[1], o[1]) / total >= 0.80:
            print("\nHigh Page Fault Rate: Possible Thrashing")
        else:
            print("\nPage Fault Rate is not excessively high.")

        choice = input("\nRun again with different frame count? (y/n): ")

        if choice.lower() != "y":
            break


main()
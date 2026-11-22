def paging():
    print("\n========== PAGING ==========")

    page_size = int(input("Enter page size: "))
    logical_address = int(input("Enter logical address: "))

    if page_size <= 0 or logical_address < 0:
        print("Invalid page size or logical address.")
        return

    page_number = logical_address // page_size
    offset = logical_address % page_size

    print("\n--- Paging Calculations ---")
    print("Logical Address:", logical_address)
    print("Page Size:", page_size)
    print("Page Number:", page_number)
    print("Offset:", offset)

    n = int(input("Enter number of page table entries: "))
    page_table = []

    for i in range(n):
        frame = int(input(f"Enter frame number for page {i} (-1 if unmapped): "))
        page_table.append(frame)

    print("\nPage Table:", page_table)

    if page_number >= n:
        print("Error: Invalid page number.")
        return

    frame_number = page_table[page_number]

    if frame_number == -1:
        print("Error: Page is not mapped in memory.")
        return

    if frame_number < 0:
        print("Error: Invalid frame number.")
        return

    physical_address = frame_number * page_size + offset

    print("\n--- Physical Address Calculation ---")
    print("Frame Number:", frame_number)
    print("Formula: Frame Number * Page Size + Offset")
    print("Calculation:", frame_number, "*", page_size, "+", offset)
    print("Physical Address:", physical_address)


def segmentation():
    print("\n========== SEGMENTATION ==========")

    segment_number = int(input("Enter segment number: "))
    offset = int(input("Enter offset: "))
    base = int(input("Enter segment base address: "))
    limit = int(input("Enter segment limit: "))

    print("\n--- Segmentation Calculations ---")
    print("Segment Number:", segment_number)
    print("Offset:", offset)
    print("Base Address:", base)
    print("Limit:", limit)

    if segment_number < 0 or offset < 0 or base < 0 or limit < 0:
        print("Error: Invalid segment values.")
        return

    if offset >= limit:
        print("Error: Offset exceeds segment limit.")
        return

    physical_address = base + offset

    print("\n--- Physical Address Calculation ---")
    print("Formula: Base Address + Offset")
    print("Calculation:", base, "+", offset)
    print("Physical Address:", physical_address)


def main():
    while True:
        print("\n====== MEMORY MANAGEMENT ======")
        print("1. Paging")
        print("2. Segmentation")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            paging()
        elif choice == "2":
            segmentation()
        elif choice == "3":
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Try again.")


main()
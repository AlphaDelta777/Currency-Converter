class ListStats:
    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2

    def average(self):
        return sum(self.list1) / len(self.list1), sum(self.list2) / len(self.list2)

    def minimum(self):
        return min(self.list1), min(self.list2)

    def maximum(self):
        return max(self.list1), max(self.list2)


def get_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)  # accepts int + double
        except ValueError:
            print("Invalid input! Please enter only integer or decimal numbers.")


def get_list(list_name):
    numbers = []
    print(f"Enter 2 numbers for {list_name}:")
    for i in range(2):
        num = get_number(f"{list_name} number {i+1}: ")
        numbers.append(num)
    return numbers


def main():
    list1 = get_list("List 1")
    list2 = get_list("List 2")

    stats = ListStats(list1, list2)

    print("\n--- Results ---")
    print("Averages:", stats.average())
    print("Minimums:", stats.minimum())
    print("Maximums:", stats.maximum())


if __name__ == "__main__":
    main()

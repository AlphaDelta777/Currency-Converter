def identity_demo():
    print("=== Identity Demo ===")

    a = [1, 2, 3]
    b = [1, 2, 3]

    print("a == b:", a == b)   # True (same values)
    print("a is b:", a is b)   # False (different objects)
    print("id(a):", id(a))
    print("id(b):", id(b))

    c = a
    print("a is c:", a is c)   # True

    c.append(4)

    print("After modifying c:")
    print("a:", a)  # changed
    print("b:", b)  # unchanged
    print("c:", c)

    print("\n")


def task_manager():
    tasks = []

    while True:
        print("\n=== Task Manager ===")
        print("1: Add task")
        print("2: List tasks")
        print("3: Exit")

        choice = input("Choose: ")

        if choice == "1":
            task = input("Enter task: ")
            tasks.append(task)
            print("Task added.")

        elif choice == "2":
            if tasks:
                print("Tasks:")
                for i, t in enumerate(tasks, 1):
                    print(f"{i}. {t}")
            else:
                print("No tasks yet.")

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")



def main():
    identity_demo()
    task_manager()


if __name__ == "__main__":
    main()
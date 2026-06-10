class ListManager:
    def __init__(self):
        self.a = [1, 2, 3]
        self.b = [1, 2, 3]
        self.c = self.a  # same object as a

    def show(self):
        print(f"a: {self.a} (id={id(self.a)})")
        print(f"b: {self.b} (id={id(self.b)})")
        print(f"c: {self.c} (id={id(self.c)})\n")

    def add(self):
        self.c.append(input("Add value: "))

    def delete(self):
        val = input("Delete value: ")
        if val in self.c:
            self.c.remove(val)

    def run(self):
        print("a == b:", self.a == self.b)
        print("a is b:", self.a is self.b)
        print("a is c:", self.a is self.c)

        while True:
            self.show()
            choice = input("1:Add  2:Delete  3:Exit → ")

            if choice == "1":
                self.add()
            elif choice == "2":
                self.delete()
            elif choice == "3":
                break


ListManager().run() 

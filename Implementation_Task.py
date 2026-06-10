class Task:
    def __init__(self, title):
        self.title = title
        self.done = False

    def mark_done(self):
        self.done = True

    def describe(self):
        status = "True" if self.done else "False"
        return f"{status} {self.title}"



task1 = Task("Have breakfast")
task2 = Task("Complete Assignment 2")
task3 = Task("Prepare the program for next week")


task3.mark_done()


print(task1.describe())
print(task2.describe())
print(task3.describe())

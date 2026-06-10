
class Student:
    def __init__(self, name, student_id, initial_grades=[]):
        """
        Initializes a new Student object.
        Bundles name, ID, and grades together.
        """
        self.name = name
        self.student_id = student_id
        self.grades = list(initial_grades) # Use a copy to avoid mutable default arg issues

    def add_grade(self, new_grade):
        """
        Adds a new grade to this student's grades list.
        The student object itself manages its grades.
        """
        self.grades.append(new_grade)
        print(f"Added grade {new_grade} for {self.name}. Current grades: {self.grades}")

    def calculate_average(self):
        """
        Calculates the average of this student's grades.
        The student object 'knows' how to calculate its own average.
        """
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def get_summary(self):
        """
        Returns a formatted summary of this student's information.
        """
        avg = self.calculate_average() # Calling a method on self
        return (f"Student: {self.name} (ID: {self.student_id})\n"
                f"Grades: {self.grades}\n"
                f"Average Score: {avg:.2f}")


alice = Student("Alice Smith", "S001", [85, 90, 78, 92])

print("--- Initial State ---")
print(alice.get_summary())

# Add a new grade - the object manages its own state
alice.add_grade(88)

print("\n--- After Adding a Grade ---")
# The object now holds the updated state internally
print(alice.get_summary())

# Change student's name directly on the object
alice.name = "Alicia Smith"
print("\n--- After Name Change ---")
print(alice.get_summary())
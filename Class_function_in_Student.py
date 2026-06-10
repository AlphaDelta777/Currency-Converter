class Student:
    def __init__(self, name, student_id, initial_grades=None):
        """
        Represents a student with a name, ID, and a list of grades.
        """
        self.name = name
        self.student_id = student_id
        self.grades = initial_grades[:] if initial_grades else []

    def add_grade(self, new_grade):
        """
        Adds a new grade after validating it.
        """
        if not isinstance(new_grade, (int, float)):
            raise ValueError("Grade must be a number.")
        if not 0 <= new_grade <= 100:
            raise ValueError("Grade must be between 0 and 100.")

        self.grades.append(new_grade)

    def calculate_average(self):
        """
        Returns the average grade, or None if no grades exist.
        """
        return sum(self.grades) / len(self.grades) if self.grades else None

    def get_summary(self):
        """
        Returns a formatted summary of the student's information.
        """
        avg = self.calculate_average()
        avg_str = f"{avg:.2f}" if avg is not None else "No grades yet"

        return (
            f"Student: {self.name} (ID: {self.student_id})\n"
            f"Grades: {self.grades}\n"
            f"Average Score: {avg_str}"
        )


# --- Demonstration of Usage ---

# Create an instance of the Student class
James = Student("John James", "Z721", [3, 90, 87, 42])
print(James.get_summary())

# Add a new grade - to the object manages its own state
James.add_grade(54)
print("\nAfter adding a grade:")
print(James.get_summary())

# Change student's name directly on the object - to show that data and behavior are now encapsulated together
James.name = "Rick Owens"
print("\nAfter name change:")
print(James.get_summary())
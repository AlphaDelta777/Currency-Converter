#--- Data Information ---
student_name = "John Doe"
student_id = "S123456"
student_grades = [59, 21, 99, 100, 3] # List of numerical grades

#--- Function Definitions ---

def calculate_average(grades_list):
    """Calculate the average of a List grades."""
    if not grades_list:
        return 0
    return sum(grades_list) / len(grades_list)

def add_grades(grades_list, new_grade):
    """Add a new grade to the student's grades list."""
    grades_list.append(new_grade)
    print(f"Added grade {new_grade}. Current grades: {grades_list}")

def get_student_summary(name, student_id, grades_list):
    """Returns a formatted summary of the student's information"""
    avg=calculate_average(grades_list) # Calling another function
    return (f"Student: {name} (ID: {student_id})\n"
            f"Grades: {grades_list}\n"
            f"Average Score: {avg:.2f}")


print("--- Initial State ---")
print(get_student_summary(student_name, student_id, student_grades))


add_grades(student_grades, 88)

#Problem: Data and behavior are separateed.
#To see the updated average, we must explicittly call get_student_summary again.
#passing all pieces of data(name, id , and the now-modified grades list)
print("\n--- After Adding a Grade ---")
print(get_student_summary(student_name, student_id, student_grades))
      
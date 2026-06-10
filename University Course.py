class Person:
    def __init__(self, name, age, id_number):
        self._name = name
        self._age = age
        self._id_number = id_number
    
    def get_info(self):
        return f"Name: {self._name} | Age: {self._age} | ID: {self._id_number}"

class Course:
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name
        self.instructor = None
        self.enrolled_students = []

class Student(Person):
    def __init__(self, name, age, id_number, major, gpa):
        super().__init__(name, age, id_number) # super() usage
        self._major = major
        self._gpa = float(gpa)
        self._enrolled_courses = []
        
    def enroll_in_course(self, course):
        if course not in self._enrolled_courses:
            self._enrolled_courses.append(course)
            course.enrolled_students.append(self)
            return True
        return False

    def get_info(self):
        # Overriding base method
        base_info = super().get_info()
        codes = [c.course_code for c in self._enrolled_courses]
        return f"[Student] {base_info} | Major: {self._major} | GPA: {self._gpa} | Courses: {codes if codes else 'None'}"

class Professor(Person):
    def __init__(self, name, age, id_number, department):
        super().__init__(name, age, id_number) # super() usage
        self._department = department
        self._courses_teaching = []
        
    def assign_to_course(self, course):
        if course not in self._courses_teaching:
            self._courses_teaching.append(course)
            course.instructor = self

    def get_info(self):
        base_info = super().get_info()
        codes = [c.course_code for c in self._courses_teaching]
        return f"[Professor] {base_info} | Dept: {self._department} | Teaching: {codes if codes else 'None'}"


def main():
    students = {}
    professors = {}
    courses = {}

    while True:
        print("\n=== University System Menu ===")
        print("1. Register Student")
        print("2. Hire Professor")
        print("3. Add Course to Catalog")
        print("4. Assign Professor to Course")
        print("5. Enroll Student in Course")
        print("6. Show System Directory")
        print("7. Exit")
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == "1":
            name = input("Student Name: ")
            age = int(input("Age: "))
            id_num = input("Student ID (Unique): ")
            major = input("Major: ")
            gpa = float(input("GPA: "))
            students[id_num] = Student(name, age, id_num, major, gpa)
            print(f"Success: Registered {name}.")
            
        elif choice == "2":
            name = input("Professor Name: ")
            age = int(input("Age: "))
            id_num = input("Faculty ID (Unique): ")
            dept = input("Department: ")
            professors[id_num] = Professor(name, age, id_num, dept)
            print(f"Success: Hired Prof. {name}.")
            
        elif choice == "3":
            code = input("Course Code (Unique): ")
            title = input("Course Title: ")
            courses[code] = Course(code, title)
            print(f"Success: Added {code} to catalog.")
            
        elif choice == "4":
            p_id = input("Enter Faculty ID: ")
            c_code = input("Enter Course Code: ")
            if p_id in professors and c_code in courses:
                professors[p_id].assign_to_course(courses[c_code])
                print("Success: Faculty assigned to course.")
            else:
                print("Error: Invalid Faculty ID or Course Code.")
                
        elif choice == "5":
            s_id = input("Enter Student ID: ")
            c_code = input("Enter Course Code: ")
            if s_id in students and c_code in courses:
                if students[s_id].enroll_in_course(courses[c_code]):
                    print("Success: Student enrolled.")
                else:
                    print("Notice: Student already enrolled.")
            else:
                print("Error: Invalid Student ID or Course Code.")
                
        elif choice == "6":
            print("\n--- System Registry Directory ---")
            for p in professors.values():
                print(p.get_info())
            for s in students.values():
                print(s.get_info())
            
            print("\n--- Active Course Catalog ---")
            if not courses:
                print("No courses cataloged.")
            for c in courses.values():
                inst = f"Prof. {c.instructor._name}" if c.instructor else "TBD"
                print(f"{c.course_code}: {c.course_name} (Instructor: {inst} | Enrolled: {len(c.enrolled_students)})")
                
        elif choice == "7":
            print("Exiting system dashboard. Goodbye!")
            break
        else:
            print("Invalid input choice. Please try again.")

if __name__ == "__main__":
    main()
class Course:
    def __init__(self, course_code: str, course_name: str, max_capacity: int, credit_hours: int):
        self.course_code = course_code
        self.course_name = course_name
        self.max_capacity = max_capacity
        self.credit_hours = credit_hours
        self.enrolled_students = []  

    @property
    def has_space(self) -> bool:
        """
        Using @property turns this method into a getter attribute.
        We can now check 'course.has_space' instead of calling 'course.has_space()'.
        """
        return len(self.enrolled_students) < self.max_capacity

    def add_student(self, student) -> bool:
        """Adds a student to the roster if space permits."""
        if self.has_space: 
            self.enrolled_students.append(student)
            return True
        return False

    def __str__(self):
        return f"{self.course_code}: {self.course_name} ({len(self.enrolled_students)}/{self.max_capacity} Students)"


class Student:
    def __init__(self, student_id: str, name: str, max_credits: int = 15):
        self.student_id = student_id
        self.name = name
        self.max_credits = max_credits
        self.current_courses = []  # List to track courses this student is taking

    @property
    def total_credits(self) -> int:
        """
        Using @property dynamically computes the credit load on the fly
        while treating it like a simple data variable.
        """
        return sum(course.credit_hours for course in self.current_courses)

    def can_take_course(self, course: Course) -> bool:
        """Validation helper: Checks if adding the course exceeds credit limits."""
        return self.total_credits + course.credit_hours <= self.max_credits

    def enroll(self, course: Course) -> str:
        """
        Coordinates the enrollment process. 
        Note: Validation happens here by checking BOTH student and course constraints.
        """
 # 1: Prevent duplicate enrollment
        if course in self.current_courses:
            return f"X {self.name} is already enrolled in {course.course_code}."
        
#  2: Validate student credit capacity
        if not self.can_take_course(course):
            return f"X Enrollment failed: {self.name} would exceed maximum credit limit ({self.max_credits} credits)."
        
 # 3: Validate course seat capacity
        if not course.has_space:
            return f"X Enrollment failed: {course.course_code} is full."

 # If all validations pass, mutate the states of both objects
        course.add_student(self)
        self.current_courses.append(course)
        return f"✅ {self.name} successfully enrolled in {course.course_code}."

if __name__ == "__main__":
    print("--- Setting up System Entities ---")
    algo_101 = Course("CS101", "Algorithms", max_capacity=2, credit_hours=4)
    data_202 = Course("CS202", "Data Structures", max_capacity=3, credit_hours=4)
    python_301 = Course("CS301", "Advanced Python", max_capacity=5, credit_hours=4)
    
    John = Student("S001", "John", max_credits=7)
    var_bob = Student("S002", "Bob", max_credits=15)
    Andy = Student("S003", "Andy", max_credits=15)

    print("\n--- Simulating Enrollment & Validation ---")
    
    print(John.enroll(algo_101))
    print(var_bob.enroll(algo_101)) 
    
    print(Andy.enroll(algo_101)) 
    
    print(John.enroll(data_202)) 

    print(var_bob.enroll(data_202)) 
    
    print("\n--- Final Status Report ---")
    print(algo_101)
    print(data_202)
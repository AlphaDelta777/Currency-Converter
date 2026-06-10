from Course_Registration_System import Course, Student

def create_test_data():
    """Generates a fresh set of data before every test run."""
    courses = {
        "algo": Course("CS101", "Algorithms", max_capacity=2, credit_hours=4),
        "data": Course("CS202", "Data Structures", max_capacity=3, credit_hours=4)
    }
    John = Student("S001", "John", max_credits=7)
    bob = Student("S002", "Bob", max_credits=15)
    
    return courses, John, bob

def test_successful_enrollment():
    courses, _, bob = create_test_data()
    algo = courses["algo"]
    
    response = bob.enroll(algo)
    
    assert "successfully enrolled" in response
    assert algo in bob.current_courses
    assert bob in algo.enrolled_students


def test_duplicate_enrollment_validation():
    courses, _, bob = create_test_data()
    algo = courses["algo"]
    
    bob.enroll(algo)
    duplicate_response = bob.enroll(algo)
    
    assert "already enrolled" in duplicate_response
    assert len(bob.current_courses) == 1


def test_course_capacity_limit_validation():
    courses, John, bob = create_test_data()
    algo = courses["algo"]
    charlie = Student("S003", "Charlie", max_credits=15)
    
    John.enroll(algo)
    bob.enroll(algo)
    fail_response = charlie.enroll(algo)
    
    assert "is full" in fail_response
    assert charlie not in algo.enrolled_students
    assert len(algo.enrolled_students) == 2


def test_student_credit_limit_validation():
    courses, John, _ = create_test_data()
    algo = courses["algo"]
    data = courses["data"]
    
    John.enroll(algo)
    fail_response = John.enroll(data)
    
    assert "exceed maximum credit limit" in fail_response
    assert data not in John.current_courses
    assert John not in data.enrolled_students

if __name__ == "__main__":
    print("--- Running Registration System Tests ---")
    
    tests = [
        test_successful_enrollment,
        test_duplicate_enrollment_validation,
        test_course_capacity_limit_validation,
        test_student_credit_limit_validation
    ]
    
    passed_count = 0
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}: PASSED")
            passed_count += 1
        except AssertionError as e:
            print(f"X {test.__name__}: FAILED")
            
    print("\n-----------------------------------------")
    print(f"Results: {passed_count}/{len(tests)} tests passed.")
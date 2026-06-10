import streamlit as st
from University_Course import Student, Professor, Course

def Student_Streamlit():
    st.title("University Course Registration System")
    
    courses = {
        "CS101": Course("CS101", "Algorithms"),
        "CS202": Course("CS202", "Data Structures")
    }
    
    professors = {
        "Dr. Smith": Professor("Dr. Smith", 45, "P001", "Computer Science"),
        "Dr. Johnson": Professor("Dr. Johnson", 50, "P002", "Computer Science")
    }
    
    students = {
        "Alice": Student("Alice", 20, "S001", "Computer Science", 3.8),
        "Bob": Student("Bob", 22, "S002", "Computer Science", 3.5)
    }
    
    professors["Dr. Smith"].assign_to_course(courses["CS101"])
    professors["Dr. Johnson"].assign_to_course(courses["CS202"])

    st.header("Courses and Instructors")
    for course in courses.values():
        instructor_name = course.instructor._name if course.instructor else "TBA"
        st.write(f"{course.course_code}: {course.course_name} | Instructor: {instructor_name}")

    st.header("Student Enrollment")
    student_name = st.selectbox("Select Student:", list(students.keys()))
    course_code = st.selectbox("Select Course to Enroll:", list(courses.keys()))
    
    if st.button("Enroll"):
        student = students[student_name]
        course = courses[course_code]
        result = student.enroll_in_course(course)
        
        if result:
            st.success(f"{student_name} successfully enrolled in {course_code}.")
        else:
            st.error(f"{student_name} is already enrolled in {course_code}.")

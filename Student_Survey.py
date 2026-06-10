import streamlit as st


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
        super().__init__(name, age, id_number)
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
        base_info = super().get_info()
        codes = [c.course_code for c in self._enrolled_courses]
        return f"[Student] {base_info} | Major: {self._major} | GPA: {self._gpa} | Courses: {codes if codes else 'None'}"

class Professor(Person):
    def __init__(self, name, age, id_number, department):
        super().__init__(name, age, id_number)
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


st.set_page_config(layout="wide")
st.title("University System Portal")

# Initialize central data stores
for key in ["students", "professors", "courses"]:
    if key not in st.session_state:
        st.session_state[key] = {}

st.sidebar.header("Registrar Admin Panel")
action_type = st.sidebar.selectbox("Create Entity", ["Student", "Professor", "Course"])

name = st.sidebar.text_input("Name / Course Title")
id_num = st.sidebar.text_input("ID / Course Code (Unique)")
age = st.sidebar.number_input("Age", 17, 90, 25) if action_type != "Course" else 0

if action_type == "Student":
    major = st.sidebar.text_input("Major")
    gpa = st.sidebar.slider("GPA", 0.0, 4.0, 3.5, 0.1)
    if st.sidebar.button("Register Student") and id_num and name:
        st.session_state.students[id_num] = Student(name, age, id_num, major, gpa)
        st.rerun()

elif action_type == "Professor":
    dept = st.sidebar.text_input("Department")
    if st.sidebar.button("Hire Professor") and id_num and name:
        st.session_state.professors[id_num] = Professor(name, age, id_num, dept)
        st.rerun()

elif action_type == "Course":
    if st.sidebar.button("Add to Catalog") and id_num and name:
        st.session_state.courses[id_num] = Course(id_num, name)
        st.rerun()


col1, col2 = st.columns(2)

with col1:
    st.header("System Directory")
    
    if not st.session_state.professors and not st.session_state.students and not st.session_state.courses:
        st.info("System is empty. Use the sidebar menu to populate data.")
        
    for prof in st.session_state.professors.values():
        st.text(prof.get_info())
    for student in st.session_state.students.values():
        st.text(student.get_info())
        
    if st.session_state.courses:
        st.subheader("Course Catalog")
        for c in st.session_state.courses.values():
            inst = f"Prof. {c.instructor._name}" if c.instructor else "TBD"
            st.markdown(f"**{c.course_code}**: {c.course_name} (Instructor: {inst} | Enrolled: {len(c.enrolled_students)})")

with col2:
    st.header("System Operations")

    if st.session_state.professors and st.session_state.courses:
        st.subheader("Assign Instructor")
        p_choices = {f"Prof. {p._name} ({p._id_number})": p for p in st.session_state.professors.values()}
        c_choices = {f"{c.course_code} - {c.course_name}": c for c in st.session_state.courses.values()}
        
        sel_prof = st.selectbox("Select Faculty", list(p_choices.keys()), key="op_p")
        sel_crs = st.selectbox("Select Course Target", list(c_choices.keys()), key="op_c1")
        
        if st.button("Confirm Faculty Assignment"):
            p_choices[sel_prof].assign_to_course(c_choices[sel_crs])
            st.rerun()
            
    if st.session_state.students and st.session_state.courses:
        st.subheader("Enroll Student")
        s_choices = {f"{s._name} ({s._id_number})": s for s in st.session_state.students.values()}
        c_choices_2 = {f"{c.course_code} - {c.course_name}": c for c in st.session_state.courses.values()}
        
        sel_stud = st.selectbox("Select Student", list(s_choices.keys()), key="op_s")
        sel_crs_2 = st.selectbox("Select Course Target", list(c_choices_2.keys()), key="op_c2")
        
        if st.button("Confirm Enrollment"):
            s_choices[sel_stud].enroll_in_course(c_choices_2[sel_crs_2])
            st.rerun()
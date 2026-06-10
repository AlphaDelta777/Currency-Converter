import json
import os
import streamlit as st

class Student:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades
    
    def to_dict(self):
        """Convert to dictionary for JSON"""
        return {
            'name': self.name,
            'age': self.age,
            'grades': self.grades
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            data['name'],
            data['age'],
            data['grades']
        )

st.title("🎓 Student JSON Serialization Roundtrip")
st.write("Modify the student details below to test saving (serializing) and loading (deserializing) data.")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Input Student Data")
    
    name = st.text_input("Student Name", value="Hugo")
    age = st.number_input("Age", min_value=1, max_value=120, value=20)

    grades_input = st.text_input("Grades (comma-separated)", value="85, 80, 88")
    try:
        grades = [int(g.strip()) for g in grades_input.split(",") if g.strip()]
    except ValueError:
        st.error("Please enter valid integers separated by commas.")
        grades = []

    if st.button("Serialize & Save to JSON "):
        if grades:
            # Create object and serialize
            student = Student(name, age, grades)
            with open('student.json', 'w') as f:
                json.dump(student.to_dict(), f, indent=2)
            st.success("Successfully saved to `student.json`!")
        else:
            st.error("Cannot save without valid grades.")

with col2:
    st.header("2. Deserialize & Verify")
    
    if st.button("Load from JSON & Deserialize "):
        if os.path.exists('student.json'):
            # Read and Deserialize
            with open('student.json', 'r') as f:
                loaded_data = json.load(f)
                loaded_student = Student.from_dict(loaded_data)
            
            # Display Raw JSON
            st.subheader("Raw JSON File Content:")
            st.json(loaded_data)
            
            # Display Reconstructed Object Properties
            st.subheader("Reconstructed Python Object:")
            st.write(f"**Name:** {loaded_student.name}")
            st.write(f"**Age:** {loaded_student.age}")
            st.write(f"**Grades:** {loaded_student.grades}")
            
            # Verification logic
            st.success("✅ Roundtrip Verification Complete!")
        else:
            st.warning("No `student.json` file found. Save some data on the left first!")
            
            
            

import json

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

# Save
student = Student("Hugo", 20, [85, 80, 88])
with open('student.json', 'w') as f:
    json.dump(student.to_dict(), f, indent=2)
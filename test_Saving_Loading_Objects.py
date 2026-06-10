import json
import pytest
from Saving_Loading_Objects import Student



def test_student_serialization_roundtrip():
    original_student = Student("James", 20, [85, 80, 88])

    json_string = json.dumps(original_student.to_dict())
    loaded_data = json.loads(json_string)
    loaded_student = Student.from_dict(loaded_data)
    
    assert loaded_student.name == original_student.name
    assert loaded_student.age == original_student.age
    assert loaded_student.grades == original_student.grades
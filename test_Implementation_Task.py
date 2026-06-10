from Implementation_Task import Task

def test_mark_done():
    task = Task("Test task")
    task.mark_done()
    assert task.done is True

def test_describe_not_done():
    task = Task("Complete Assignment 2")
    assert task.describe() == "False Complete Assignment 2"

def test_describe_done():
    task = Task("Prepare the program for next week")
    task.mark_done()
    assert task.describe() == "True Prepare the program for next week"

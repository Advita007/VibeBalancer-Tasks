class Student:
    def __init__(self,name,rollno,marks):
        self.name = name 
        self.rollno = rollno
        self.marks = marks

    def status(self):
        if self.marks>=40:
            print("Passed")
        else:
            print("Failed")

name = input("Enter the name: ")
rollno = input("Roll no.: ")
marks = int(input("Marks: "))
print("Student Details: \n")
student = Student(name,rollno,marks)
print(student.name)
print(student.rollno)
print(student.marks)
student.status()

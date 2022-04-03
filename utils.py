from db.models import Student
import cv2
from pyzbar import pyzbar

def read_barcodes():
    
    cam = cv2.VideoCapture(0)
    barcode_info = ''
    while True:
        result, frame = cam.read()

        cv2.imshow('Barcode Capture', frame)

        barcodes = pyzbar.decode(frame)
        
        key = cv2.waitKey(10)

        if key & 0xFF == ord('q'):
            break

        if len(barcodes) == 1:
            barcode_info = barcodes[0].data.decode('utf-8')
            break
        else:
            continue

    cam.release()
    cv2.destroyAllWindows()
    return barcode_info


def get_reg_number():
    student_reg_number = input("Enter Student's registration number: ")

    try:
        Student.objects.get(reg_number=student_reg_number)
    except:
        print("Student Enrollment")
        first_name = input("Enter student's first name: ")
        last_name = input("Enter student's last name: ")
        level_of_study = input("Enter student's level of study: ")
        new_student = Student(reg_number=student_reg_number, first_name=first_name,
                    last_name=last_name, level_of_study=level_of_study)
        new_student.save()
    else:
        print("Update Student Enrollment")
        student = Student.objects.get(reg_number=student_reg_number)
        print(student)

    return student_reg_number.replace("/", "_")

def get_reg_number_verify():

    """Function for getting student registration number for verification"""

    # student_reg_number = input("Enter Student's registration number: ")
    student_reg_number = read_barcodes()

    try:
        Student.objects.get(reg_number=student_reg_number)
    except:
        print("Student not enrolled yet")
        return True
    else:
        print("Student verification")
        student = Student.objects.get(reg_number=student_reg_number)
        print(student)

    return student_reg_number.replace("/", "_")


import os
from picamera.array import PiRGBArray
from picamera import PiCamera
from db.models import Student
from utils import get_reg_number, get_reg_number_verify
import cv2
import face_recognition
import numpy as np
import time

def face_enrol():
    reg_number = get_reg_number()
    student = Student.objects.get(reg_number=reg_number.replace('_', '/'))
    # reg_number = 'test_image'
    #initialize the camera
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 32
    raw_capture = PiRGBArray(cam, size=(640,480))
    
    time.sleep(0.1)
    for frame in cam.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        
        
        raw_capture.truncate(0)
        
        if key == ord("q"):
            break

        if  key == ord('c'):
            os.makedirs(os.path.dirname(f"{reg_number}/"), exist_ok=True)
            cv2.imwrite(f"{reg_number}/{reg_number}.png", image)
            saved_image = face_recognition.load_image_file(f"{reg_number}/{reg_number}.png")
            #if len(saved_image) > 1:
             #   print("More than one face in captured image")
            try:
                saved_image_encoding = face_recognition.face_encodings(saved_image)[0]
            except IndexError:
                print("No face detected in saved image")
                quit()
            student.face_encodings = Student.face_enc_to_str(saved_image_encoding)
            student.save()
            print(f"Record for {student.last_name} ,{student.first_name} saved")
            break
    cam.stop_preview()
    cam.close()
    cv2.destroyAllWindows()

def face_verify():
    reg_number = get_reg_number_verify()
    student = Student.objects.get(reg_number=reg_number.replace('_','/'))

    # Initialize the camera
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 32
    raw_capture = PiRGBArray(cam, size=(640,480))
    
    time.sleep(0.1)
    for frame in cam.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        
        
        raw_capture.truncate(0)
        
        if key == ord("q"):
            break

        if  key == ord('c'):
            cv2.imwrite("temp.png", image)
            break
    
    cam.stop_preview()
    cam.close()
    cv2.destroyAllWindows()
 
    captured_image = face_recognition.load_image_file("temp.png")
    
    try:
        captured_img_enc = face_recognition.face_encodings(captured_image)[0]
    except IndexError:
        print("No face detected in captured image")
        return True
    
    saved_encoding = Student.str_to_face_enc(student.face_encodings)

    if face_recognition.compare_faces([saved_encoding], captured_img_enc):
        print(f"Face Match: {student.last_name}, {student.first_name}")
    else:
        print(f"Face did not match with records for {student.last_name}, {student.first_name}")
    # break
    return False

# 
# def face_identify():
# 
#     # initialize the webcam
#     video_capture = cv2.VideoCapture(0)
# 
#     # create an array of face encodings of all students in database
#     all_students = list(Student.objects.exclude(face_encodings__isnull=True).exclude(face_encodings__exact=''))
#     all_students_face_enc = list(enc for enc in [Student.str_to_face_enc(item.face_encodings) for item in all_students])
# 
#     face_locations = []
#     face_encodings = []
#     face_names = []
#     process_this_frame = True
# 
#     while True:
#         # Grab a single frame of video
#         result, frame = video_capture.read()
# 
#         # Resize frame of video to 1/4 size for faster face recognition processing
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
# 
#         # Convert the image from BGR color (which openCV uses) to RGB color
#         rgb_small_frame = small_frame[:, :, ::-1]
# 
#         # only process every other frame of video to save time
#         if process_this_frame:
#             # Find all the faces and face encodings in the current frame of video
#             face_locations = face_recognition.face_locations(rgb_small_frame)
#             face_encodings = face_recognition.face_encodings(
#                                             rgb_small_frame, face_locations)
# 
#             face_names = []
#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(
#                                         all_students_face_enc, face_encoding)
#                 name = "Unknown"
# 
#                 face_distances = face_recognition.face_distance(
#                                         all_students_face_enc, face_encoding)
#                 best_match_index = np.argmin(face_distances)
#                 if matches[best_match_index]:
#                     name = f"{all_students[best_match_index].reg_number} {all_students[best_match_index].last_name}, {all_students[best_match_index].first_name}"
#                 
#                 face_names.append(name)
# 
#         process_this_frame = not process_this_frame
# 
#         for (top, right, bottom, left), name in zip(face_locations, face_names):
#             # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4
# 
#             # Draw a box around the face
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
# 
#             # Draw a label with a name below the face
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (left + 6, bottom -6), font, 1.0, (255, 255, 255), 1)
#         
#         cv2.imshow('Video', frame)
# 
#         # Hit 'q' on the keyboard to quit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     video_capture.release()
#     cv2.destroyAllWindows()
#     return True

while True:
    print("\n\nFACE DEMO -----")
    
    print("e) Enrol Student")
    print("v) Verify existing student")
    print("i) Identify students in live video feed [[Invigilation mode]]")
    print("q) Quit")
    print("========================")
    c = input("> ")

    if c == "q":
        print("Exiting demo program")
        raise SystemExit

    if c == "e":
        face_enrol()
    
    if c == "v":
        face_verify()
#     
#     if c == "i":
#         face_identify()
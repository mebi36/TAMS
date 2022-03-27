from fileinput import filename
import time
import serial
from PIL import Image

import adafruit_fingerprint


uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_sensor_storage_slot():
    i = -1
    while(i > finger.library_size - 1) or ( i < 0):
        try:
            i = int(input(f"Enter Sensor storage slot # from 0-{finger.library_size - 1}"))
        except ValueError:
            pass
    return i

def get_reg_number():
    student_reg_number = input("Enter Student's registration number: ")
    student_reg_number = student_reg_number.replace("/", "_")
    return student_reg_number


def fingerprint_enrol():
    reg_number = get_reg_number()
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="", flush=True)
        else:
            print("Place same finger again...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False
        
        print("Tempating...",end="",flush=True)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False
        
        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    i = finger.create_model()
    if i ==  adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model for %s " % reg_number, end="", flush=True)


    ###creating image
    print("\nPlace finger one more time")
    while finger.get_image():
        pass
    
    img = Image.new("L", (256, 288), "white")
    pixeldata = img.load()
    mask = 0b00001111
    result = finger.get_fpdata(sensorbuffer="image")

    x = 0
    y = 0

    for i in range(len(result)):
        pixeldata[x, y] = (int(result[i]) >> 4) * 17
        x += 1
        pixeldata[x, y] = (int(result[i]) & mask) * 17
        if x == 255:
            x = 0
            y += 1
        else:
            x += 1
    try:
        img.save(f"{reg_number}.png")
    except:
        print("Problem saving image")

    ###creating template file
    data = finger.get_fpdata("char", 1)
    with open(f"{reg_number}.dat", "wb") as file:
        file.write(bytearray(data))
    print("Template saved...")

    return True

def fingerprint_verification():
    reg_number = get_reg_number()
    print("Waiting for finger print...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False

    print("Loading file template...", end="", flush=True)
    with open(f"{reg_number}.dat", "rb") as file:
        data = file.read()
    finger.send_fpdata(list(data), "char", 2)

    i = finger.compare_templates()
    if i == adafruit_fingerprint.OK:
        print("Fingerprint match template in file.")
        return True
    if i == adafruit_fingerprint.NOMATCH:
        print("Templates do not match!")
    else:
        print("Other error!")
    return False



while True:
    print("FINGERPRINT DEMO ----")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    if finger.count_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    #if finger.set_sysparam(6, 2) != adafruit_fingerprint.OK:
     #   raise RuntimeError("Unable to set package size to 128!")
    if finger.read_sysparam() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to get system parameters")
    print("e) enroll finger print")
    print("v) verify exisiting record")
    print("q) quit")
    print("==================")
    c = input("> ")

    if c == "q":
        print("Exiting demo program")
        raise SystemExit
    
    if c == "e":
        fingerprint_enrol()
    if c == "v":
        fingerprint_verification()
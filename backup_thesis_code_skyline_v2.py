import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import pyttsx3
import threading
import time
import easyocr
from PIL import Image
from geopy.geocoders import Nominatim
import reverse_geocoder as rg
import serial
import pynmea2
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
engine = pyttsx3.init()
alarm_sound = pyttsx3.init()
voices = alarm_sound.getProperty('voices')
alarm_sound.setProperty('voice', 'english+f2')
alarm_sound.setProperty('rate', 140)

### VOICE RECONGITION FUNCTION


def speak_text1(text):
    try:
        alarm_sound = pyttsx3.init()
        alarm_sound.say(text)
        alarm_sound.runAndWait()
    except:
        pass
    
def speak_text2(text1, text2):
    try:
        alarm_sound = pyttsx3.init()
        alarm_sound.say(text1 + text2)
        alarm_sound.runAndWait()
    except:
        pass    
def run_thread1(text):
    try:
        
        thread = threading.Thread(target=speak_text1, args=(text,))
        thread.start()
    except:
        pass
    

def run_thread2(text1, text2):
    try:
            
        thread = threading.Thread(target=speak_text2, args=(text1, text2))
        thread.start()
    except:
        pass

 
def locationalarm(alarm_sound):

    while True:
        try:
            port="/dev/ttyAMA0"
            ser=serial.Serial(port, baudrate=9600, timeout=0.5)
            dataout = pynmea2.NMEAStreamReader()
            newdata=ser.readline().decode('unicode_escape')


            if newdata[0:6] == "$GPRMC":
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
    #             print(gps)
                coordinates = (lat,lng)
                results = rg.search(coordinates) # default mode = 2
    #             print(results)
                for i in results:
                    name1 = i['name']
                    admin1 = i['admin1']
                    print (name1, admin1)
#                     run_thread1("Gps Signal Lost")
                    
                    if name1 == 'Takoradi' and admin1 == 'Western':
                        print("Gps Signal Lost")
                        run_thread1("Gps Signal Lost")
                        
                    else:
                        run_thread2(name1,admin1)
                        
 
                        
                        
                break
                

    #             engine = pyttsx3.init()
    #             engine.say(results)
    #             engine.runAndWait()
        except:
            continue


    

run_thread1("Hello. To Activate the Text Recognition. Press Button 1. To activate GPS Location. Press Button 2, your system, is now, detecting")
### OBJECT DETECTION FUNCTION
def detection():
    

    path_hubconfig = r'/home/pi/Project Thesiss/yolov5'# path ng yolov5
    path_trained_model = r'/home/pi/Project Thesiss/pinakafinalmodel.pt' #Our model
    model = torch.hub.load(path_hubconfig, 'custom', path=path_trained_model, source='local')
#     cap = cv2.VideoCapture('http://192.168.1.66:8080/video')
#     width = 640
#     height = 480
    cap = cv2.VideoCapture(0)
#     cap.set(3,640)
#     cap.set(4,480)





    while True:
        try:
            ret, frame = cap.read()
#             frame = cv2.resize(frame, (width, height))

            model.conf = 0.35

        # Make detections 
            results = model(frame)

            labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
            
            labels1, cord = results.xyxyn[0][:, -2], results.xyxyn[0][:, :-2]
            
#             print (labels1)
#             print (labels)
           
#             print(labels1)#confidence


            cv2.imshow('YOLO', np.squeeze(results.render()))


    #         if labels <=0:
    #             print ("no detect")

    #         labels, cord = results

            
            n = len(labels)
#             print(n)#class
       
          

            for i in range(len(labels)):
                for obj in range(len(labels1)):
#                     print(labels)
                

                    if labels[i] == 0 and labels1[obj] >= 0.75:

                        print ("book")
                        run_thread1("Book Detected")

                       
                        
                    if labels[i] == 1 and labels1[obj] >= 0.75:

                        print ("Computer")
                        run_thread1("Computer Detected")
                    if labels[i] == 2 and labels1[obj] >= 0.75:

                        print ("Electric Fan")
                        run_thread1("Electric Fan Detected")

                    if labels[i] == 3 and labels1[obj] >= 0.75:

                        print ("Phone")
                        run_thread1("Phone Detected")

                    if labels[i] == 4 and labels1[obj] >= 0.50:

                        print ("Table")
                        run_thread1("Table Detected")

                    if labels[i] == 5 and labels1[obj] >= 0.45:

                        print ("Text")
                        run_thread1("Text Detected")


   
                    
                    ###describing the two classify##
                    
                    if 0 in labels and 5 in labels and labels1[obj] >= 0.60:
                        print ("Book and Texts")
                        run_thread1("There are Text, on. a Book")

                    if 1 in labels and 4 in labels and labels1[obj] >= 0.60:
                        print ("Computer and Table")
                        run_thread1("There are computer, on. a table")
                    
                    if 3 in labels and 4 in labels and labels1[obj] >= 0.60:
                        print ("Phone and Table")
                        run_thread1("There are Phone, on. a table")
                        
                    
#                     if 3 in labels and 5 in labels and labels1[obj] >= 0.50:
#                         print ("Phone and Text")
#                         run_thread1("There are Text, on. a Phone")
                        
                

                    


        except:
             continue
    #     if n >= 1:
    #         print ("detect object")
    #     else:
    #         print (" multiple object")

        k = cv2.waitKey(1)


###QUIT BUTTONS
#         if k == ord('1'):
        if GPIO.input(23) == GPIO.LOW or k == ord('1'): #button GPIO 23

            cap.release()
            cv2.destroyAllWindows()
            time.sleep(2)
            run_thread1("Activating Text Recognition")

          #  camera = cv2.VideoCapture('http://192.168.1.39:8080/video')
#             width = 480
#             height = 272
            width = 480
            height = 272
            camera = cv2.VideoCapture(0)
#             camera.set(3,640)
#             camera.set(4,480)
            while True:
                _,image=camera.read()
                image = cv2.resize(image, (width, height))
                ##
        

                cv2.imshow('text detection', image)
#                 if cv2.waitKey(1)& 0xFF ==ord("1"):
                if cv2.waitKey(1)& GPIO.input(23) == GPIO.LOW or cv2.waitKey(1)& 0xFF ==ord("1"):

                    time.sleep(1.5)
                    
                    run_thread1("Captured! Please wait for a while. it processing the text. To Activate Text recognition. Press button 1. To activate Gps Location. Press Button 2.")

                    cv2.imwrite(r'/home/pi/Downloads/shot.jpg',image)
                    break
            camera.release()
            cv2.destroyAllWindows()
            tesseract()
            detection()
            
            
            break
        if GPIO.input(24) == GPIO.LOW or k ==ord('2'):

#         if k ==ord('2'):
            run_thread1("Searching GPS")

            time.sleep(3)
            cap.release()
            cv2.destroyAllWindows()

            locator()
            time.sleep(2)
            detection()
        if k == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            

#             button3()
            
            break

    cap.release()
    cv2.destroyAllWindows()
    
    
#without bounding box

    

#text recognition

def tesseract():
    try:
        reader = easyocr.Reader(['en'])
        IMAGE_PATH = r'/home/pi/Downloads/shot.jpg'
        result = reader.readtext(IMAGE_PATH)
        
        if not result: # If no text is detected
            run_thread1("No text detected")
            return
        
        top_left = tuple(result[0][0][0])
        bottom_right = tuple(result[0][0][2])
        text = result[0][1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.imread(IMAGE_PATH)
        spacer = 100
        for detections in result: 
            
            top_left = tuple(detections[0][0])
            bottom_right = tuple(detections[0][2])
            text = detections[1]
            img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)
            img = cv2.putText(img,text,(20,spacer), font, 1,(255,255,0),2,cv2.LINE_AA)
            spacer+=30
            print(text)
            alarm_sound = pyttsx3.init()
            alarm_sound.say(text)
            alarm_sound.runAndWait()
            cv2.imwrite(r'/home/pi/Downloads/result.jpg',img)

    except:
        print("Error occurred while processing image.")        
        
        
        

            
def locator():
    
    alarm = threading.Thread(target=locationalarm, args=(alarm_sound,))
    alarm.start()
   







detection()






import cv2
import numpy as np
import time
import change
import paho.mqtt.client as mqtt
import dcmotor

mesg = ""



def shapeDetection():
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connect returned result code: " + str(rc))


    def on_message(client, userdata, msg):
        print(msg.payload.decode("utf-8"))
        global mesg
        mesg = msg.payload.decode("utf-8")
        
    
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message


    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)


    client.username_pw_set("admin", "password")


    client.connect("broker", 8883)


    client.subscribe("mydevice")

    client.loop_start()
 

    def nothing(x):
        pass

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Settings")

    cv2.createTrackbar("Lower-Hue", "Settings", 0, 180, nothing)
    cv2.createTrackbar("Lower-Saturation", "Settings", 0, 255, nothing)
    cv2.createTrackbar("Lower-Value", "Settings", 0, 255, nothing)
    cv2.createTrackbar("Upper-Hue", "Settings", 0, 180, nothing)
    cv2.createTrackbar("Upper-Saturation", "Settings", 0, 255, nothing)
    cv2.createTrackbar("Upper-Value", "Settings", 0, 255, nothing)

    font = cv2.FONT_HERSHEY_SIMPLEX

    while 1:
        x=0
        ret, frame = cap.read()
        frame = frame[100:500,100:500]
        frame = cv2.flip(frame, 1)
        blur = cv2.GaussianBlur(frame, (5, 5), 1)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        lh = cv2.getTrackbarPos("Lower-Hue", "Settings")
        ls = cv2.getTrackbarPos("Lower-Saturation", "Settings")
        lv = cv2.getTrackbarPos("Lower-Value", "Settings")
        uh = cv2.getTrackbarPos("Upper-Hue", "Settings")
        us = cv2.getTrackbarPos("Upper-Saturation", "Settings")
        uv = cv2.getTrackbarPos("Upper-Value", "Settings")

        """lower_color = np.array([lh, ls, lv])
        upper_color = np.array([uh, us, uv])"""
        
        lower_color = np.array([0, 0, 21])
        upper_color = np.array([21, 255, 255])
        
        
        mask = cv2.inRange(hsv, lower_color, upper_color)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel)

        _,contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            
        for cnt in contours:
            area = cv2.contourArea(cnt)

            epsilon = 0.015 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if area > 400:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

                if len(approx) == 4:
                    cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
                    
                    change.changeOnes()

                else :
                    cv2.putText(frame, "Distorted shape", (x, y), font, 1, (0, 0, 0))
                    change.changeZeros()
                                             
                    
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)

        if cv2.waitKey(3) & 0xFF == ord('q'):
                       
            break
        if mesg =="stop":
            dcmotor.motorStop()
            break
        
    cap.release()
    cv2.destroyAllWindows()
import pigpio
import time

pi = pigpio.pi()

servo_pin = 26

def servoStart():
    pi.set_servo_pulsewidth(servo_pin,1100)
    
   
def servoStop():
     pi.set_servo_pulsewidth(servo_pin,550)
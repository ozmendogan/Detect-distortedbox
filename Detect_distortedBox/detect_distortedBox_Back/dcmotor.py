import pigpio
import time

pi = pigpio.pi()
pwm_pin = 17               #ENA pin
in1 = 23  
in2 = 24

def motorStart():
    pi.set_mode(in1,pigpio.OUTPUT)
    pi.set_mode(in2,pigpio.OUTPUT)
    pi.write(in1,0)
    pi.write(in2,1)


    pi.set_PWM_frequency(pwm_pin,60)
    pi.set_PWM_dutycycle(pwm_pin,33)



def motorStop():
    pi.set_PWM_dutycycle(pwm_pin,0)
    pi.write(in1,0)
    pi.write(in2,0)
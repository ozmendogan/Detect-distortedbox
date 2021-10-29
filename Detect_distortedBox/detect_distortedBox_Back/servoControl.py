import change
import servo
import time

while True:
	x=  change.readValue()
   
   

        if x==str("1"):
        	print("1")
        	time.sleep(0.5)
        	servo.servoStop()
                time.sleep(0.5)
                servo.servoStart()
                change.changeOnes()
   
      	elif x==str("0"):
                print("0")
                servo.servoStart()
  
        
        
    
        
    











        
        
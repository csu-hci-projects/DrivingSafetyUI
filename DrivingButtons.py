import RPi.GPIO as GPIO
import time

#seconds between buttons checking
intervaltime = 0.5
#radio on/off variable
radio = 0
#volume variable in % of maximum volume
volume = 50

#GPIO
ButtonIn1 = 21
ButtonIn2 = 20
ButtonIn3 = 26
ButtonIn4 = 19
ButtonIn5 = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(relay, GPIO.OUT)

#activate output
def activate(pin):
    GPIO.output(pin, GPIO.HIGH)

def deactivate(pin):
    GPIO.output(pin, GPIO.LOW)

#Main code
try:
    while(True):
        #Push-to-activate buttons
        if(GPIO.input(ButtonIn1)):
            #TODO: Speech button
        if(GPIO.input(ButtonIn2)):
            #TODO: Call/Hang Up Button
        if(GPIO.input(ButtonIn3)):
            #Volume up button
            volume = volume + 10
        if(GPIO.input(ButtonIn4)):
            #Volume down button
            volume = volume - 10
            
        #Latch button functions
        if(GPIO.input(ButtonIn5)):
            #Radio on/off
            radio = 1
        else:
            radio = 0
        
        #LOGIC FOR FUNCTIONALITY GOES HERE
        
        #delay between update checks
        time.sleep(intervalTime)
#Allow the program to exit at any time
except KeyboardInterrupt:
    print("Quiting program and cleaning up.")

#Clean up
GPIO.cleanup()
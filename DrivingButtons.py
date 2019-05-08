import RPi.GPIO as GPIO
import time

#seconds between buttons checking
intervalTime = 0.5
#radio on/off variable
radio = 0
#volume variable in % of maximum volume
volume = 50

#GPIO
ButtonIn1 = 21
ButtonIn2 = 20
ButtonIn3 = 16
ButtonIn4 = 19
ButtonIn5 = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(ButtonIn1, GPIO.IN)
GPIO.setup(ButtonIn2, GPIO.IN)
GPIO.setup(ButtonIn3, GPIO.IN)
GPIO.setup(ButtonIn4, GPIO.IN)
GPIO.setup(ButtonIn5, GPIO.IN)
#GPIO.setup(relay, GPIO.OUT)

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
            print("Button 1 pressed!")
            #TODO: Speech button
            time.sleep(intervalTime)
        if(GPIO.input(ButtonIn2)):
            print("Button 2 pressed!")
            #TODO: Call/Hang Up Button
            time.sleep(intervalTime)
        if(GPIO.input(ButtonIn3)):
            #Volume up button
            print("Button 3 pressed")
            volume = volume + 10
            time.sleep(intervalTime)
        if(GPIO.input(ButtonIn4)):
            #Volume down button
            print("Button 4 pressed")
            volume = volume - 10
            time.sleep(intervalTime)
        #Latch button functions
        if(GPIO.input(ButtonIn5)):
            #Radio on/off
            print("radio on")
            radio = 1
            time.sleep(intervalTime)
        else:
            radio = 0
        
        #LOGIC FOR FUNCTIONALITY GOES HERE
        
        #delay between update checks
        #time.sleep(intervalTime)
#Allow the program to exit at any time
except KeyboardInterrupt:
    print("Quiting program and cleaning up.")

#Clean up
GPIO.cleanup()

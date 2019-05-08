import RPi.GPIO as GPIO
import time
import alsaaudio
import pygame
import os
import random
import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    print("Getting devices...")
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        #Ding to let the user know the microphone is listening
        pygame.mixer.music.load("dings.mp3")
        pygame.mixer.music.play()
        print("Listening...")
        #This does not limit the amount of time listened
        audio = recognizer.listen(source)
        print("Finished listening")

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    print("Transcribing...")
    
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
        
    print("Finished transcribing.")
    return response

if __name__ == "__main__":
    print("Program started")
    #seconds between buttons checking
    intervalTime = 0.5
    #radio on/off variables
    radio = 0
    #volume variable; default 48%
    volume = 90
    #Call on/off variable
    call = 0

    #GPIO
    ButtonIn1 = 21
    ButtonIn2 = 20
    ButtonIn3 = 16
    ButtonIn4 = 19
    ButtonIn5 = 13

    #Set buttons input to GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ButtonIn1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ButtonIn2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ButtonIn3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ButtonIn4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ButtonIn5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(ButtonIn1, GPIO.IN)
    #GPIO.setup(ButtonIn2, GPIO.IN)
    #GPIO.setup(ButtonIn3, GPIO.IN)
    #GPIO.setup(ButtonIn4, GPIO.IN)
    #GPIO.setup(ButtonIn5, GPIO.IN)
    
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    #microphone = sr.Microphone() #sr.Microphone.list_microphone_names() to get list of Microphone // sr.Microphone(device_index=3) to specify a microphone to use'
    microphone = sr.Microphone(device_index=2) #Top right USB port
    
    #initialize pygame
    pygame.mixer.init()
    
    #Ding to say devices loaded
    #pygame.mixer.music.load("trained.mp3")
    #pygame.mixer.music.play()
    print("Devices recognized.")
    print(sr.Microphone.list_microphone_names())
    
    
    #Set up volume comtrol
    mixer = alsaaudio.Mixer('PCM')
    #sets initial volume to 48%
    mixer.setvolume(volume)

    #activate output
    def activate(pin):
        GPIO.output(pin, GPIO.HIGH)

    def deactivate(pin):
        GPIO.output(pin, GPIO.LOW)

    #Main code
    try:
        while(True):
            #, GPIO.input(ButtonIn2), GPIO.input(ButtonIn3), GPIO.input(ButtonIn4), GPIO.input(ButtonIn5))
            #Push-to-activate buttons
            if(GPIO.input(ButtonIn1)):
                print("Button 1 (Speech Recognition Button) pressed!")
                #Speech button
                pygame.mixer.pause()
                #pygame.mixer.stop()
                word = recognize_speech_from_mic(recognizer, microphone)
                if word["transcription"] != None:
                    word = word["transcription"].lower()
                else:
                    word = None
                print("Transcription complete")
                
                # show the user the transcription
                print("You said: {}".format(word))

                if word == None:
                    #Set value to be read to user
                    text = "I was not able to hear that."
                elif word == "volume up":
                    if(volume < 100):
                        volume = volume + 2
                        mixer.setvolume(volume)
                    text = "Volume raised"
                elif word == "volume down":
                    if(volume > 0):
                        volume = volume - 2
                        mixer.setvolume(volume)
                    text = "Volume lowered"
                elif word == "call":
                    if(call == 0):
                        text = "Who would you like to call?"
                        os.system("flite -t \"" + text + "\"")
                        name = recognize_speech_from_mic(recognizer, microphone)
                        name = name["transcription"].lower()
                        text = "Calling " + name
                        call = 1
                    else:
                        text = "You are already in a call. Press the phone button to hang up."
                elif word == "text":
                    text = "Who would you like to text?"
                    os.system("flite -t \"" + text + "\"")
                    name = recognize_speech_from_mic(recognizer, microphone)
                    name = name["transcription"].lower()
                    text = "What would you like to text " + name + "?"
                    os.system("flite -t \"" + text + "\"")
                    message = recognize_speech_from_mic(recognizer, microphone)
                    message = message["transcription"].lower()
                    text = "Message sent to " + name + ": " + message
                else:
                    text = "I do not have a command for " + word
                #Play text-to-speech back to user 
                os.system("flite -t \"" + text + "\"")
                pygame.mixer.unpause()
                time.sleep(intervalTime)
            if(GPIO.input(ButtonIn2)):
                print("Button 2 (Call Button) pressed!")
                #Call/Hang Up Button
                if call == 0:
                    call = 1
                    os.system("flite -t \"Call accepted\"")
                else:
                    call = 0
                    os.system("flite -t \"Call ended\"")
                time.sleep(intervalTime)
            if(GPIO.input(ButtonIn3)):
                #Volume up button
                print("Button 3 (Volume Up) pressed")
                if(volume < 100):
                    volume = volume + 2
                    mixer.setvolume(volume)
                time.sleep(intervalTime)
            if(GPIO.input(ButtonIn4)):
                #Volume down button
                print("Button 4 (Volume Down) pressed")
                if(volume > 0):
                    volume = volume - 2
                    mixer.setvolume(volume)
                time.sleep(intervalTime)
            #Latch button functions
            if(GPIO.input(ButtonIn5)):
                #Radio on/off
                if(radio != 1):
                    print("Radio On")
                    radio = 1
                    pygame.mixer.music.load("Beethoven.mp3")
                    pygame.mixer.music.play()
                time.sleep(intervalTime)
            else:
                if(radio != 0):
                    print("Radio Off")
                    radio = 0
                    #pygame.mixer.stop()
                    pygame.mixer.music.load("empty.mp3")
                    pygame.mixer.music.play()
            
            #delay between update checks
            #time.sleep(intervalTime)
    #Allow the program to exit at any time
    except KeyboardInterrupt:
        print("Quiting program and cleaning up.")

    #Clean up
    GPIO.cleanup()


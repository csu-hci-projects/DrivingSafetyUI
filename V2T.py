#install pip if you don't have it
#pip install SpeechRecognition
#sudo apt-get install python-pyaudio python3-pyaudio

from gtts import gTTS #pip install gTTS
  
# This module is imported so that we can  
# play the converted audio 
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
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone() #sr.Microphone.list_microphone_names() to get list of Microphone // sr.Microphone(device_index=3) to specify a microphone to use
    language = 'en'

    word =recognize_speech_from_mic(recognizer, microphone)
    # show the user the transcription
    print("You said: {}".format(word["transcription"]))

    #if word["transcription"] == "text":
    text =" you said " + word["transcription"].lower()
    myobj = gTTS(text=text, lang=language, slow=False) 
    myobj.save("success.mp3") 
  
    # Playing the converted file 
    os.system("mpg321 success.mp3")

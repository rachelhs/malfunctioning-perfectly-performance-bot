# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import speech_recognition as sr
import time

def recognise_question_from_speech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        #https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst
        #timeout is how long it will listen for if nothing is detected (None means no limit)
        timeout = None
        phrase_time_limit = 5
        audio = r.listen(source, timeout, phrase_time_limit)
        #audio = r.listen(source)
        print("processing")

    # recognize speech using Google speech to text
    try:
        text = u""+str(r.recognize_google(audio))
        print('Heard: {}'.format(text))
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Google error; {0}".format(e))

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-service-account/tokyo-comfort-320610-e45e3b8edd50.json'

    if ("chronically" in text) | ("chronic" in text) | ("late" in text):
        result = 'chronically_late'
        print('chronically_late')
    elif ("study" in text):
        result = 'help_study'
        print('help_study')
    elif ("Do you take ADHD medication" in text | "meth" in text):
        result = 'adhd_medication'
        print('adhd_medication')
    
    return result

audience_question = recognise_question_from_speech()
import sys
import os
import time
from PIL import Image, ImageDraw, ImageFont, ImageColor
import cv2
import random
import numpy as np

# imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import speech_recognition as sr

#set initial age and gender states
audience_speech = 'unknown'
fontsize = 23
generate_green_background = True

# listens for audience question
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
        text = 'unknown'
    except sr.RequestError as e:
        print("Google error; {0}".format(e))
        text = 'unknown'

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-service-account/tokyo-comfort-320610-e45e3b8edd50.json'

    if ("chronically" in text) | ("chronic" in text) | ("late" in text):
        result = 'chronically_late'
        print('chronically_late')
    elif ("study" in text):
        result = 'help_study'
        print('help_study')
    elif ("do you take ADHD medication" in text) | ("meth" in text):
        result = 'adhd_medication'
        print('adhd_medication')
    elif("feel like" in text) | ("first went on" in text):
        result = 'first_feel_like_medication'
        print('first_feel_like_medication')
    elif("what is it like" in text) | ("to have ADHD" in text):
        result = 'what_is_it_like'
        print('what_is_it_like')
    elif("goodbye" in text):
        result = 'end'
        print('end')
    else:
        result = 'unknown'
    
    return result, text

#draw background for display (mode, (w, h), colour)
canvas = Image.new('RGB', (800, 600), (255, 255, 255))

#for writing text to screen
def GenerateText(size, fontsize, bg, fg, text):
	#generate a piece of canvas and draw text on it
	canvas = Image.new('RGB', size, bg)
	draw = ImageDraw.Draw(canvas)
	grotesk = ImageFont.truetype("fonts/PxGrotesk-Screen.otf", fontsize)
	#first parameter is top left corner of text
	draw.text((0, 0), text, fg, font=grotesk)
	#change to BGR for opencv
	return cv2.cvtColor(np.array(canvas), cv2.COLOR_RGB2BGR)

def set_background():
	# sets white background image with target gender highlighted and static text
	global background
	background = cv2.imread('plain-white-background.jpeg')	

set_background()

#create fullscreen
cv2.namedWindow("Target", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Target",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

#display target age and target gender
def display_target_cat():
	audience_speech_text = GenerateText((800, 20), 12, 'white', 'black', f"{audience_speech}")
	background[0: 20 ,0: 800] = audience_speech_text

display_target_cat()

while(True):
    
    time.sleep(3)
    result, audience_speech = recognise_question_from_speech()
    print(audience_speech)
    set_background()
    display_target_cat()
    cv2.imshow('Target', background)
		
    if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

cv2.destroyAllWindows()
# this is program is a virtual assistant that will give the time, the date, a greeting and give basic information
# on people

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

#ignore any warning messages that we get in the program
warnings.filterwarnings("ignore")

#record audio and return it as a string
def record_audio():
    #record the audio
    r = sr.Recognizer() #create a recognizer object

    #open the microphone and record
    with sr.Microphone() as source:
        print("say something...")
        audio = r.listen(source)

    #use Google's speech recognition
    data = ""
    try:
        data = r.recognize_google(audio)
        print(f"you said: {data}")
    except sr.UnknownValueError: #Check for unknow errors:
        print("Google Speech Recognition did not recognize the audio")
    except sr.RequestError as e:
        print(f"Google results from Speech Recognition service error: {e}")

    return data


#function to the virtual assistance response
def assistant_response(text):
    print(text)
    #convert the text to the speech
    my_obj = gTTS(text=text, lang='en', slow=False)
    # save the converted text to a file
    my_obj.save("assistant_response.mp3")
    #play the converted file
    os.system("start assistant_response.mp3")

#a function for awake word or phrase
def wake_word(text):
    WAKE_WORDS = ['hi laptop', 'okay laptop', 'hey laptop'] #list of wake phrases
    text = text.lower() #converting text to all lowercase letters
    #check to see if user's text contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    #executed only if wake work is not found in the loop
    return False
#function to get current date
def get_date():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()] #gets the current day ie Sunday
    month_num = now.month
    day_num = now.day
    year = now.year

    # list of months
    1

    month_names = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
                 'August', 'September', 'October', 'November', 'December']

    #list of oridinal numbers
    oridinal_numbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
     '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
     '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th',
     '29th', '30th', '31st']

    return f"Today is {weekday}, {month_names[month_num - 1]} the {oridinal_numbers[day_num - 1]}, {year} "

# function to get a rondom greeting response
def greeting(text):

    #greeting inputs
    GREETING_INPUTS = ['hi', 'hello', 'hola', 'whats up', 'how are you']

    #greeting response
    GREETING_RESPONSES = ['howdy', 'whats going on', 'hey there', 'welcome back', ]

    #check if user input a greeting then return a randomly chosen response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES + '.')

    #if no greeting is detected return an empty string
    return ""

# a function to get a persons first and last name
def get_person(text):
    word_list = text.split() #splitting the text into a list of words
    for i in range(0, len(word_list)):
        if i + 3 <= len(word_list) - 1 and word_list[i].lower() == 'who' and word_list[i + 1].lower() == 'is':
            return word_list[i+2] + ' ' + word_list[i +3]

while True:
    # record audio
    text = record_audio()
    response = ''

    #check for wake word
    if(wake_word(text) == True):
        #Check for greeting by the user
        response = response + greeting(text)
        #Check to see if the user ask for the date
        if('date' in text):
            getDate = get_date()
            response = response + "" + getDate

        #Check to see if the user wants the time
        if('time' in text):
            now = datetime.datetime.now()
            meridiem = ""
            if now.hour >= 12:
                meridiem = "p.m." #post meridiem
                hour = now.hour - 12
            else:
                meridiem = "a.m." #ante meridiem
                hour = now.hour
            #convert minute into a string
            if now.minute < 10:
                minute = f"0{str(now.minute)}"
            else:
                minute = f"{str(now.minute)}"

            response = f"{response} It is {str(hour)}:{minute} {meridiem}"

        #check to see if the user says 'who is'
        if("who is" in text):
            person = get_person(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response +" "+ wiki

        #the asssistant will respond back with audio
        assistant_response(response)






import speech_recognition as sr
import pyttsx3
import webbrowser
import openai 
import os
import datetime


engine = pyttsx3.init()
engine.setProperty('rate', 150)

text = "Hello I am Jarvis AI"
print(text)

engine.say(text)
engine.runAndWait()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....") 
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}")
        return query 
    except Exception as e:
        print("Sorry, could not understand.")
        return ""
 
if __name__ =='__main__':
    print("Vs Code")
    say("Hello I am Jarvis AI")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["chatgpt", "https://www.chatgpt.com"]]
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]} mam...")
                webbrowser.open(site[1])
        if "open photos" in query.lower(): 
            photosPath = r"C:\Users\Paragya\OneDrive\Pictures"
            os.startfile(photosPath)
        
        if "the time" in query.lower(): 
           strTime = datetime.datetime.now().strftime("%H:%M:%S")
           say(f"the time is {strTime}")
           print(strTime)
        
            
        # if query:
        #     say("Opening YouTube...") 
  
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def say(text):
    engine.say(text)
    engine.runAndWait()
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration = 1)
        try:
            audio = r.listen(source, timeout = 10, phrase_time_limit=8)
            query = r.recognize_google(audio,language = "en-in")
            print("You said:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            print("Error:", e)
            return ""
        
if __name__ == "__main__":
    while True:
        text = takeCommand()
        if "NOVA" in text:
            say("Yes, I am listening")
            print("Wake word detected!")
            break
        else:
            print("Say NOVA to wake me up...")

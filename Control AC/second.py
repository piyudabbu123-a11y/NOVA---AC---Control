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
    with sr.Microphone(device_index=1) as source:  # laptop mic
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        say("Listening")

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print("You said:", query)
            return query.lower()

        except sr.WaitTimeoutError:
            print("No speech detected")
            say("I did not hear anything")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""

if __name__ == "__main__":
    say("Hello I am NOVA")
    text = takeCommand()
    print(f"Command received: {text}")
    if text:
        say(f"You said {text}")
        
        
            
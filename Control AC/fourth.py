import pyttsx3
import datetime

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def say(text):
    engine.say(text)
    engine.runAndWait()
    
def greet():
    hour = datetime.datetime.now().hour
    print(f"Current hour : {hour}")
    
    if 0 <= hour < 12:
        say("Good Morning! I am NOVA, How can help you")
        print("Good Morning!")
    elif 12 <= hour < 17:
        say("Good Afternoon! I am NOVA, How can I help you")
        print("Good Afternoon!")
    elif 17 <= hour < 21:
        say("Good Evening! I am NOVA, How can I help you")
        print("Good Evening!")
    else:
        say("Good Night! I am NOVA, How can I help you")
        print("Good Night!")


if __name__ == '__main__':
    greet()
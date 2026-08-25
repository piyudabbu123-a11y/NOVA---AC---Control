import pyttsx3


engine = pyttsx3.init()


engine.setProperty('rate', 140)      
engine.setProperty('volume', 1.0)

# Voice selection
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

# Speak function
def say(text):
    engine.say(text)
    engine.runAndWait()

# Test
if __name__ == '__main__':
    say("Hello. I am NOVA, your personal AC assistant")
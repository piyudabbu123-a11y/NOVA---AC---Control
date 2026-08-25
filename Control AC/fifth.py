import pyttsx3
import speech_recognition as sr
import threading


ac_on = False
current_temp = 24
default_temp = 24
timer = None

def say(text):
    print("NOVA:", text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def takeCommand(timeout=10):
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=10)
                             
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print("You said:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""

def resetTemp():
    global current_temp
    current_temp = default_temp
    print(f"Auto reset! Temperature back to {default_temp}°C")

def startTimer():
    global timer
    if timer is not None:
        timer.cancel()
    timer = threading.Timer(60, resetTemp)
    timer.start()

def askTemperature():
    global current_temp
    say("What temperature do you want?")
    text = takeCommand(timeout=5)

    if text:
        words = text.split()
        for word in words:
            if word.isdigit():
                current_temp = int(word)
                say(f"Sure! Setting temperature to {current_temp} degrees. I will reset it to {default_temp} degrees after 15 minutes.")
                print(f"Temperature set to {current_temp}°C")
                startTimer()
                return

    current_temp = default_temp
    say(f"No problem! Running at default {default_temp} degrees.")
    print(f"Default temp: {default_temp}°C")

def handleCommand(text):
    global ac_on, current_temp, timer

    if "turn on" in text:
        if ac_on:
            say("AC is already on!")
        else:
            ac_on = True
            print("AC ON")
            say("Sure! Turning on the AC.")
            askTemperature()

    elif "turn off" in text:
        if not ac_on:
            say("AC is already off!")
        else:
            ac_on = False
            if timer is not None:
                timer.cancel()
            print("AC OFF")
            say("Okay! Turning off the AC. Have a great day!")

    elif "change temperature" in text:
        if ac_on:
            words = text.split()
            for word in words:
                if word.isdigit():
                    current_temp = int(word)
                    say(f"Done! Temperature changed to {current_temp} degrees. Timer has been reset.")
                    print(f"Temperature changed to {current_temp}°C")
                    startTimer()
                    break
        else:
            say("Please turn on the AC first!")

    elif "status" in text:
        if ac_on:
            say(f"AC is currently on at {current_temp} degrees.")
            print(f"AC ON | Temp: {current_temp}°C")
        else:
            say("AC is currently off.")

    elif "hello" in text or "hi" in text:
        say("Hello! I am Nova, your personal AC assistant. How can I help you?")

    elif "thank" in text:
        say("You are welcome! Always here to help.")

    else:
        say("Sorry, I did not understand that command.")

if __name__ == "__main__":
    say("Hello! I am NOVA, your personal AC assistant. I am ready to help you.")

    print("\nAvailable Commands:")
    print("- Turn on AC")
    print("- Turn off AC")
    print("- Change temperature 21")
    print("- Status")
    print("- Hello\n")

    while True:
        text = takeCommand()
        if text:
            handleCommand(text)
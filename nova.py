import speech_recognition as sr
import threading
import datetime
from ui import updateUI, startUI, root, setListening
import pygame
import os
import tempfile
import asyncio
import edge_tts
import tempfile

ac_on        = False
current_temp = 24
default_temp = 24
timer        = None
user_lang    = "en"  


def say(text):

    print("NOVA:", text)

    root.after(
        0,
        lambda: updateUI(
            ac_on,
            current_temp,
            log=text
        )
    )

    voice = "en-IN-NeerjaNeural"

    if user_lang == "hi":
        voice = "hi-IN-SwaraNeural"

    async def speak_edge():

        tmp = tempfile.mktemp(".mp3")

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice
        )

        await communicate.save(tmp)

        pygame.mixer.init()
        pygame.mixer.music.load(tmp)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(8)

        pygame.mixer.quit()

    asyncio.run(speak_edge())
   
ENGLISH_LINES = {
    "greeting_morning": "Good Morning! I am NOVA, your smart AC assistant.",
    "greeting_afternoon": "Good Afternoon! I am NOVA, your smart AC assistant.",
    "greeting_evening": "Good Evening! I am NOVA, your smart AC assistant.",
    "greeting_night": "Good Night! I am NOVA, your smart AC assistant.",

    "ask_language": "Please select your language. Say English or Hindi.",

    "selected_english": "English selected. I am NOVA, your smart AC assistant. How can I help you?",

    "selected_hindi": "Hindi selected.",

    "already_on": "AC is already on!",
    "turning_on": "Sure! Turning on the AC.",
    "ask_temp": "What temperature do you want?",
    "temp_set": "Setting temperature to {t} degrees. Will reset after 15 minutes.",
    "default_temp": "Running at default 24 degrees.",

    "already_off": "AC is already off!",
    "turning_off": "Okay! AC turned off. Have a great day!",

    "temp_changed": "Temperature changed to {t} degrees.",

    "turn_on_first": "Please turn on the AC first!",

    "status_on": "AC is on at {t} degrees.",
    "status_off": "AC is currently off.",

    "hello_reply": "Hello! How can I help you?",
    "thanks_reply": "You are welcome! Always here to help.",

    "not_understood": "Sorry, I did not understand that command.",

    "listening": "Yes, I am listening.",

    "going_sleep": "Going to sleep. Say Nova to wake me up.",

    "task_done": "Task completed. Going back to sleep.",

    "no_command": "I could not hear your command."
  }
HINDI_LINES = {

    "greeting_morning": "Suprabhat! Main NOVA hoon, aapki smart AC assistant.",
    "greeting_afternoon": "Namaskar! Main NOVA hoon, aapki smart AC assistant.",
    "greeting_evening": "Shubh Sandhya! Main NOVA hoon, aapki smart AC assistant.",
    "greeting_night": "Shubh Ratri! Main NOVA hoon, aapki smart AC assistant.",

    "ask_language": "Kripya bhasha chuniye. English ya Hindi boliye.",

    "selected_english": "English chun li gayi hai.",

    "selected_hindi": "Hindi chunaa gaya. Main NOVA hoon, aapki smart AC assistant. Main aapki kaise madad kar sakti hoon?",

    "already_on": "AC pehle se chalu hai!",
    "turning_on": "Bilkul! AC chalu kar rahi hoon.",
    "ask_temp": "Aap kaun sa temperature chahte hain?",
    "temp_set": "Temperature {t} degree set kar rahi hoon. 15 minute baad wapas aayegi.",
    "default_temp": "Default 24 degree par chal rahi hoon.",

    "already_off": "AC pehle se band hai!",
    "turning_off": "Theek hai! AC band kar di. Aapka din shubh ho!",

    "temp_changed": "Temperature {t} degree kar di gayi hai.",

    "turn_on_first": "Pehle AC chalu karein!",

    "status_on": "AC {t} degree par chalu hai.",
    "status_off": "AC abhi band hai.",

    "hello_reply": "Namaste! Main aapki kaise madad kar sakti hoon?",

    "thanks_reply": "Koi baat nahi! Hamesha aapki seva mein hoon.",

    "not_understood": "Maafi chahti hoon, mujhe samajh nahi aaya.",

    "listening": "Haan, main sun rahi hoon.",

    "going_sleep": "So rahi hoon. Mujhe jagane ke liye Nova bolein.",

    "task_done": "Kaam ho gaya. Wapas so rahi hoon.",

    "no_command": "Mujhe aapka command sunai nahi diya."
}  

COMMANDS = {

    "turn_on": {
        "en": [
            "turn on",
            "ac on"
        ],
        "hi": [
            "ac chalu",
            "chalu karo",
            "chalu kar",
            "on karo",
            "on kar",
            "chalao"
        ]
    },

    "turn_off": {
        "en": [
            "turn off",
            "ac off"
        ],
        "hi": [
            "ac band",
            "band karo",
            "band kar",
            "off karo",
            "off kar"
        ]
    },

    "change_temp": {
        "en": [
            "change temperature",
            "temperature change",
            "set temperature"
        ],
        "hi": [
            "temperature badlo",
            "badlo",
            "temperature set",
            "degree karo",
            "degree set"
        ]
    },

    "status": {
        "en": [
            "status",
            "check"
        ],
        "hi": [
            "kitna",
            "kaisa",
            "kya chal raha",
            "temperature batao",
            "ac ka haal"
        ]
    },

    "hello": {
        "en": [
            "hello",
            "hi",
            "hii",
            "hlo",
            "hey"
        ],
        "hi": [
            "namaste",
            "namaskar"
        ]
    },

    "thanks": {
        "en": [
            "thank",
            "thanks"
        ],
        "hi": [
            "shukriya",
            "dhanyavaad"
        ]
    },
    
    "language": {
        "en": [
            "english",
            "english language",
            "speak english",
            "english mode"
        ],

        "hi": [
            "hindi",
            "हिंदी",
            "हिंदी में",
            "hindi me",
            "hindi bolo",
            "hindi main",
            "hindi language"
        ]
    }
}


def L(key, **kwargs):
    if user_lang == "hi":
        text = HINDI_LINES[key]
    else:
        text = ENGLISH_LINES[key]

    for k, v in kwargs.items():
        text = text.replace("{" + k + "}", str(v))

    return text

def takeCommand(timeout=10):
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 250

  

    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        root.after(0, lambda: setListening(True))
        r.pause_threshold = 2.0
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=10)
            root.after(0, lambda: setListening(False))
            print("Recognizing...")
            try:
                query = r.recognize_google(audio, language="en-IN")
            except:
                query = r.recognize_google(audio, language = "hi-IN")
            print("You said:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            root.after(0, lambda: setListening(False))
            return ""
        except Exception as e:
            root.after(0, lambda: setListening(False))
            print("Error:", e)
            return ""

def greet():
    hour = datetime.datetime.now().hour
    if   0  <= hour < 12: say(L("greeting_morning"))
    elif 12 <= hour < 17: say(L("greeting_afternoon"))
    elif 17 <= hour < 21: say(L("greeting_evening"))
    else:                 say(L("greeting_night"))


def selectLanguage():
    global user_lang

    say(
        ENGLISH_LINES["ask_language"]+
        " " + 
        HINDI_LINES["ask_language"])  
    text = takeCommand(timeout=8)

    if not text:
        
        user_lang = "en"
        say(L("selected_english"))
        return

    
    hindi_triggers = ["hindi", "हिंदी", "हिंदी में", "hindi me",
                      "hindi bolo", "hindi main", "hindi me baat"]
  
    english_triggers = ["english", "english mein", "english me",
                        "english bolo", "angrezi", "अंग्रेजी" ]

    if any(h in text for h in hindi_triggers):
        user_lang = "hi"
        say(L("selected_hindi"))
    
    elif any(e in text for e in english_triggers):
        user_lang = "en"
        say(L("selected_english"))
    else:
        user_lang = "en"
        say(L("selected_english"))


def resetTemp():
    global current_temp, ac_on
    current_temp = default_temp
    print(f"Auto reset to {default_temp}°C")
    root.after(0, lambda: updateUI(ac_on, current_temp))

def startTimer():
    global timer
    if timer is not None:
        timer.cancel()
    timer = threading.Timer(900, resetTemp)
    timer.start()


def askTemperature():
    global current_temp
    say(L("ask_temp"))
    text = takeCommand(timeout=6)
    if text:
        words = text.split()
        for word in words:
            if word.isdigit():
                current_temp = int(word)
                say(L("temp_set", t=current_temp))
                root.after(0, lambda: updateUI(ac_on, current_temp, timer_seconds=900))
                startTimer()
                return
    current_temp = default_temp
    say(L("default_temp"))
    root.after(0, lambda: updateUI(ac_on, current_temp))


def handleCommand(text):
    global ac_on, current_temp, timer, user_lang


    if any(w in text for w in 
           COMMANDS["turn_on"] ["en"] +
           COMMANDS["turn_on"] ["hi"]):
        if ac_on:
            say(L("already_on"))
        else:
            ac_on = True
            root.after(0, lambda: updateUI(ac_on, current_temp))
            say(L("turning_on"))
            askTemperature()

    elif any(w in text for w in 
           COMMANDS["turn_off"] ["en"] +
           COMMANDS["turn_off"] ["hi"]): 
        if not ac_on:
            say(L("already_off"))
        else:
            ac_on = False
            if timer is not None:
                timer.cancel()
            root.after(0, lambda: updateUI(ac_on, current_temp))
            say(L("turning_off"))

    elif any(w in text for w in 
           COMMANDS["change_temp"] ["en"]+
           COMMANDS["change_temp"] ["hi"]):
        if ac_on:
            words = text.split()
            for word in words:
                if word.isdigit():
                    current_temp = int(word)
                    say(L("temp_changed", t=current_temp))
                    root.after(0, lambda: updateUI(ac_on, current_temp,
                                                   timer_seconds=900))
                    startTimer()
                    return
           
            askTemperature()
        else:
            say(L("turn_on_first"))

    elif any(w in text for w in 
           COMMANDS["status"] ["en"]+
           COMMANDS["status"] ["hi"]):
        if ac_on:
            say(L("status_on", t=current_temp))
        else:
            say(L("status_off"))

    elif any(w in text for w in  
           COMMANDS["hello"] ["en"]+
           COMMANDS["hello"] ["hi"]):
        say(L("hello_reply"))

    elif any(w in text for w in 
           COMMANDS["thanks"] ["en"]+
           COMMANDS["thanks"] ["hi"]):
        say(L("thanks_reply"))
        
    
    elif any(w in text for w in 
        COMMANDS["language"]["hi"]):
        user_lang = "hi"
        say(L("Selected_hindi"))
        
    elif any(w in text for w in 
        COMMANDS["language"]["en"]):
        user_lang = "en"
        say(L("Selected_english"))   

    else:
        say(L("not_understood"))

def isWakeWord(text):
    wake_words = ["nova", "hello nova", "hey nova",
                  "no va", "nova sun", "nova suno", "नोवा", "नोवा सुनो"]
    return any(w in text for w in wake_words)

def voiceLoop():
    greet()

    selectLanguage()

  
    command = takeCommand(timeout=10)
    if command:
        handleCommand(command)

    say(L("going_sleep"))

    while True:
        print("\n── Sleeping. Waiting for wake word ──")
        text = takeCommand(timeout=None)

        if isWakeWord(text):
            say(L("listening"))
            command = takeCommand(timeout=20)

            if command:
             
                if "language" in command or "bhasha" in command:
                    selectLanguage()
                else:
                    handleCommand(command)
                say(L("task_done"))
            else:
                say(L("no_command"))


def start_voice():
    t = threading.Thread(target=voiceLoop, daemon=True)
    t.start()


if __name__ == "__main__":
    root.after(100, start_voice)
    startUI()


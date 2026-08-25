# NOVA - AC Control Assistant

NOVA is a Python-based voice-controlled AC assistant that uses speech recognition and text-to-speech to understand voice commands and provide an interactive desktop interface for AC control.

## Features

- Voice command recognition
- Text-to-speech responses (Neural TTS via Edge TTS)
- English and Hindi voice support
- Interactive desktop interface (Tkinter Canvas)
- AC ON/OFF control
- Temperature control and reset timer
- Voice-based interaction with wake word detection

## Technologies Used

- Python
- Tkinter
- SpeechRecognition
- Edge TTS
- PyGame
- psutil
- PyAudio

## Installation

Clone the repository:

```bash
git clone https://github.com/piyudabbu123-a11y/NOVA---AC---Control.git
cd NOVA---AC---Control
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python nova.py
```

## Project Structure

```text
NOVA---AC---Control/
├── nova.py              # Main NOVA application
├── ui.py                # Graphical user interface (GUI)
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── .gitignore           # Git ignore configuration
```

## Usage & Commands

1. Launch `python nova.py`.
2. Follow the spoken prompt to select your language by saying **"English"** or **"Hindi"**.
3. Wake up NOVA by saying **"Nova"** or **"Hello Nova"**.
4. Use commands such as:
   - **Turn ON / OFF**: *"Turn on the AC"* / *"AC band karo"*
   - **Set Temperature**: *"Change temperature to 21"* / *"Temperature 22 degree karo"*
   - **Check Status**: *"Status"* / *"AC ka haal"*
   - **Switch Language**: *"Change language"* / *"Bhasha badlo"*

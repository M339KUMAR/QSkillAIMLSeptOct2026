
import sys
import webbrowser
import subprocess
import pyttsx3
import speech_recognition as sr
from datetime import datetime
from urllib.parse import quote_plus

# Assistant name
ASSISTANT_NAME = "Astra"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)


# 1. SPEAK FUNCTION
def speak(text):
    print(f"\n{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()


# 2. LISTEN FUNCTION
def listen():

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            print("I'm listening...")

            recognizer.adjust_for_ambient_noise(
                source, duration=0.5
            )

            audio = recognizer.listen(
                source, timeout=5
            )

        return recognizer.recognize_google(
            audio, language="en-US"
        ).lower()

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        speak("I did not understand.")

        return ""

    except Exception as error:
        print("Microphone error:", error)

        return ""


# 3. OPEN WEBSITE FUNCTION
def open_website(url):

    if webbrowser.open(url):
        speak("Website opened.")

    else:
        speak("Unable to open the website.")


# 4. GOOGLE SEARCH FUNCTION
def search_google(query):

    webbrowser.open(
        "https://www.google.com/search?q="
        + quote_plus(query)
    )


# 5. YOUTUBE SEARCH FUNCTION
def search_youtube(query):

    webbrowser.open(
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )


# 6. OPEN APPLICATION FUNCTION
def open_application(name):

    applications = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "file explorer": "explorer.exe",
        "paint": "mspaint.exe",
        "command prompt": "cmd.exe"
    }

    if name in applications:

        try:
            subprocess.Popen(applications[name])
            speak(f"Opening {name}.")

        except OSError as error:
            speak(f"Error: {error}")

    else:
        speak("Application not configured.")

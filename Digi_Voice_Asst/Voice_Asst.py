
import sys
import webbrowser
import subprocess
import pyttsx3
import speech_recognition as sr

from datetime import datetime
from urllib.parse import quote_plus


# ==========================================
# 1. INITIALIZATION
# ==========================================

ASSISTANT_NAME = "Astra"

engine = pyttsx3.init()
engine.setProperty("rate", 175)


# ==========================================
# 2. TEXT TO SPEECH
# ==========================================

def speak(text):

    print(f"\n{ASSISTANT_NAME}: {text}")

    engine.say(text)
    engine.runAndWait()


# ==========================================
# 3. SPEECH RECOGNITION
# ==========================================

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

        command = recognizer.recognize_google(
            audio, language="en-US"
        )

        return command.lower()

    except sr.WaitTimeoutError:

        return ""

    except sr.UnknownValueError:

        speak("I did not understand.")

        return ""

    except Exception as error:

        print("Microphone error:", error)

        return ""


# ==========================================
# 4. OPEN WEBSITE
# ==========================================

def open_website(url):

    if webbrowser.open(url):

        speak("Website opened.")

    else:

        speak("Unable to open the website.")


# ==========================================
# 5. GOOGLE SEARCH
# ==========================================

def search_google(query):

    url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    webbrowser.open(url)


# ==========================================
# 6. YOUTUBE SEARCH
# ==========================================

def search_youtube(query):

    url = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )

    webbrowser.open(url)


# ==========================================
# 7. OPEN APPLICATION
# ==========================================

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


# ==========================================
# 8. PROCESS USER COMMAND
# ==========================================

def process_command(command):

    command = command.lower().strip()

    if not command:

        return True

    # Exit assistant

    if command in ["quit", "stop", "goodbye", "exit"]:

        speak("Goodbye!")

        return False


    # Website dictionary

    websites = {

        "youtube": "https://www.youtube.com",

        "facebook": "https://www.facebook.com",

        "instagram": "https://www.instagram.com",

        "whatsapp": "https://web.whatsapp.com",

        "google": "https://www.google.com",

        "github": "https://github.com",

        "gmail": "https://mail.google.com"

    }


    # Open website or application

    if command.startswith("open "):

        target = command[5:].strip()

        if target in websites:

            open_website(websites[target])

        elif target in ["chrome", "google chrome"]:

            open_website("https://www.google.com")

        elif target == "firefox":

            try:

                webbrowser.get("firefox").open(
                    "https://www.google.com"
                )

                speak("Opening Firefox.")

            except webbrowser.Error:

                speak("Firefox is not configured.")

        else:

            open_application(target)

        return True


    # Search YouTube

    if command.startswith("search youtube "):

        query = command.replace(
            "search youtube ", "", 1
        ).strip()

        if query:

            search_youtube(query)

            speak("YouTube search completed.")

        else:

            speak("Please tell me what to search.")

        return True


    # Search Google

    if command.startswith("search "):

        query = command.replace(
            "search ", "", 1
        ).strip()

        if query:

            search_google(query)

            speak("Google search completed.")

        else:

            speak("Please tell me what to search.")

        return True


    # Current time

    if any(phrase in command for phrase in [
        "what time is it",
        "current time",
        "tell me the time"
    ]):

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        speak(f"The current time is {current_time}.")

        return True


    # Today's date

    if any(phrase in command for phrase in [
        "what is the date",
        "what is today's date",
        "what day is it",
        "today's date"
    ]):

        current_date = datetime.now().strftime(
            "%d/%m/%Y"
        )

        speak(f"Today's date is {current_date}.")

        return True


    # Unknown command

    speak("Command not recognized.")

    return True


# ==========================================
# 9. MAIN FUNCTION
# ==========================================

def main():

    if sys.platform != "win32":

        print("Some commands require Windows.")

    speak(
        "Hello! I am Astra, your personal assistant."
    )


    # Select operating mode

    mode = input(
        "\nMode: 1 for Text / 2 for Voice: "
    ).strip()


    while mode not in ["1", "2"]:

        mode = input(
            "Please choose 1 for Text or 2 for Voice: "
        ).strip()


    # Continuous command processing

    while True:

        if mode == "1":

            command = input(
                "\nYou: "
            ).strip()

        else:

            command = listen()


        # Process command

        if not process_command(command):

            break


# ==========================================
# 10. EXECUTE PROGRAM
# ==========================================

if __name__ == "__main__":

    main()


# 7. MAIN PROGRAM
def main():

    speak("Hello! I am Astra, your personal voice assistant.")

    while True:

        command = listen()

        if not command:
            continue

        print("You said:", command)

        # Exit assistant
        if "exit" in command or "stop" in command:
            speak("Goodbye! Have a nice day.")
            break

        # Google search
        elif "search google" in command:
            query = command.replace("search google", "").strip()
            search_google(query)
            speak("Searching Google.")

        # YouTube search
        elif "search youtube" in command:
            query = command.replace("search youtube", "").strip()
            search_youtube(query)
            speak("Searching YouTube.")

        # Open Google
        elif "open google" in command:
            open_website("https://www.google.com")

        # Open YouTube
        elif "open youtube" in command:
            open_website("https://www.youtube.com")

        # Open applications
        elif "open calculator" in command:
            open_application("calculator")

        elif "open notepad" in command:
            open_application("notepad")

        elif "open file explorer" in command:
            open_application("file explorer")

        elif "open paint" in command:
            open_application("paint")

        elif "open command prompt" in command:
            open_application("command prompt")

        else:
            speak("Sorry, I don't know that command.")


# Execute the program
if __name__ == "__main__":
    main()

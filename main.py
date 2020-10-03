import datetime
import os
import pyttsx3
import random
import speech_recognition as speech_recognizer
import webbrowser

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 0.8)

chromePath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
browser = webbrowser.get(chromePath)

creator = "PSPK"
assistant = "Simran"


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greet_for_the_day():
    hour = int(datetime.datetime.now().hour)
    speak("Hey " + creator)
    if 0 <= hour <= 12:
        speak("Good Morning!")
    elif 12 <= hour <= 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am " + assistant + ". I hope you are safe. How can I help you?")


def listen():
    # This function takes microphone input from the user and returns String output
    recognizer = speech_recognizer.Recognizer()
    with speech_recognizer.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1  # pause_threshold ->ctrl + click to know its functionality
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        audio_text = recognizer.recognize_google(audio, language='en-IN')
        print(f"User said: {audio_text}\n")
    except Exception as e:
        # print(e)
        speak("say that again please")
        print("Say that again please...")
        return "None"
    return audio_text


def repeat_mode():
    max_repeat_idle_count = 5
    repeat_idle_count = 0
    while repeat_idle_count < max_repeat_idle_count:
        repeat_query = listen().lower()
        if repeat_query == "none":
            repeat_idle_count += 1
            continue
        elif 'quit' in repeat_query or 'bye' in repeat_query or 'exit' in repeat_query:
            speak("exiting repeat mode.")
            break
        else:
            speak(repeat_query)
            repeat_idle_count = 0
    if repeat_idle_count >= max_repeat_idle_count:
        idle_exit_helper()


def idle_exit_helper():
    speak(f"Hey {creator}, Seems like you are way. {assistant} signing off. Bye!")
    print(f"Hey {creator}, Seems like you are way. {assistant} signing off. Bye!")
    exit()


if __name__ == "__main__":
    greet_for_the_day()
    max_idle_count = 3  # Max limit for failed or empty voice recognitions.
    idle_count = 0  # track the count of failed or empty voice recognitions at time.

    # Loop until the max idle count is reached.
    while idle_count < max_idle_count:
        # Listen on microphone.
        user_voice_command = listen().lower()
        if user_voice_command == "none":
            idle_count += 1
            continue

        # Logic for executing task based on user voice command
        elif "repeat" in user_voice_command:
            speak("Entering repeat mode")
            repeat_mode()

        elif "roll a die" in user_voice_command:
            speak("Rolling....")
            speak("rrrrrrrrrrr")
            die_outcome = random.randrange(1, 6)
            speak("Here's the result: " + str(die_outcome))

        elif "search" in user_voice_command:
            webbrowser.get(chromePath).open("https://www.google.com/search?q="
                                            + user_voice_command.replace("search", "").replace(" ", "+"))
        elif "navigate" in user_voice_command:
            search_string = user_voice_command.replace("navigate", "").replace(" to ", "").replace(" ", "")  # filter
            if search_string != "":
                webbrowser.get(chromePath).open("https://www." + search_string + ".com/")
            else:
                speak(f"Sorry {creator}, I could not recognise it. Could you please repeat again.")

        elif "open google" in user_voice_command:
            webbrowser.get(chromePath).open("https://www.google.com/")

        elif "open linkedin" in user_voice_command:
            webbrowser.get(chromePath).open("https://www.linkedin.com/")

        elif "open gfg" in user_voice_command:
            webbrowser.get(chromePath).open("https://www.geeksforgeeks.org/")

        elif "open leetcode" in user_voice_command:
            webbrowser.get(chromePath).open("https://www.leetcode.com/")

        elif 'time' in user_voice_command:
            strTime = datetime.datetime.now().strftime("%H hours %M minutes %S seconds")
            speak(f"The time is {strTime}")

        elif 'open code' in user_voice_command or 'open visual studio' in user_voice_command or\
                'open vs code' in user_voice_command:
            vsPath = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(vsPath)

        elif 'who created you' in user_voice_command:
            speak("I am created by PSPK")

        elif 'who are you' in user_voice_command or 'your name' in user_voice_command:
            speak(f"I am {assistant}. A voice assistant for {creator}")

        elif "play music" in user_voice_command or "play songs" in user_voice_command:
            music_dir = 'F:\\songs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[random.randrange(0, 10)]))

        elif 'quit' in user_voice_command or 'bye' in user_voice_command or 'exit' in user_voice_command:
            speak(f"See you again {creator}. {assistant} signing off. Bye!")
            exit()

        elif user_voice_command != 'none':
            speak(f"Sorry {creator}, I could not do that. Could you please ask something else.")

        # Reset idle count;
        idle_count = 0
    if idle_count >= max_idle_count:
        idle_exit_helper()

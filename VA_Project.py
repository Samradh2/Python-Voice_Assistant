import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import yfinance as yf

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""  # Initialize the command variable
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"Recognized command: {command}")
            if 'lisa' in command:
                command = command.replace('lisa', '')
                print(f"Processed command: {command}")
            else:
                command = ""
    except sr.UnknownValueError:
        print("Sorry, I did not understand the command.")
    except sr.RequestError:
        print("Could not request results; check your network connection.")
    return command

def get_stock_summary():
    stock = yf.Ticker("^BSESN")  # BSE SENSEX
    todays_data = stock.history(period='1d')
    if not todays_data.empty:
        summary = f"Today's open was {todays_data['Open'][0]:.2f}, " \
                  f"high was {todays_data['High'][0]:.2f}, " \
                  f"low was {todays_data['Low'][0]:.2f}, " \
                  f"and close was {todays_data['Close'][0]:.2f}."
    else:
        summary = "I couldn't fetch the stock data."
    return summary

def run_lisa():
    command = take_command()
    if command:
        print(f"Running command: {command}")
        if 'play' in command:
            song = command.replace('play', '')
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        elif 'who the heck is' in command:
            person = command.replace('who the heck is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        elif 'date' in command:
            talk('sorry, I have a headache')
        elif 'are you single' in command:
            talk('I am in a relationship with wifi')
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'stock' in command:
            stock_summary = get_stock_summary()
            print(stock_summary)
            talk(stock_summary)
        else:
            talk('Please say the command again.')
    else:
        print("No command captured.")

while True:
    run_lisa()

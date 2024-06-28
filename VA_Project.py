import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import yfinance as yf
import requests

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Replace with your own Edamam API credentials if needed
EDAMAM_APP_ID = 'YOUR_APP_ID'
EDAMAM_APP_KEY = 'YOUR_APP_KEY'

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
            if 'sam' in command:
                command = command.replace('sam', '').strip()
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

def get_author_info(book_name):
    try:
        search_results = wikipedia.search(book_name)
        for result in search_results:
            page = wikipedia.page(result)
            sentences = page.summary.split('. ')
            for sentence in sentences:
                if 'author' in sentence.lower() or 'written by' in sentence.lower():
                    author_info = sentence
                    break
            else:
                author_info = "Sorry, I couldn't find information about the author of this book."
                break
    except wikipedia.DisambiguationError as e:
        author_info = f"Please be more specific, there are multiple results for {book_name}."
    except wikipedia.PageError:
        author_info = f"Sorry, I couldn't find information about the author of {book_name}."
    return author_info

def get_celebrity_info(celebrity_name):
    try:
        info = wikipedia.summary(celebrity_name, sentences=3)
    except wikipedia.DisambiguationError as e:
        info = f"Please be more specific, there are multiple results for {celebrity_name}."
    except wikipedia.PageError:
        info = f"Sorry, I couldn't find information about {celebrity_name}."
    return info

def run_sam():
    while True:
        command = take_command()
        if command:
            print(f"Running command: {command}")
            if 'stop' in command:
                print("Stopping Sam as per the command")
                talk("Goodbye!")
                break
            elif 'play' in command:
                song = command.replace('play', '').strip()
                talk('playing ' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + time)
            elif 'date' in command:
                today_date = datetime.datetime.now().strftime('%B %d, %Y')
                talk('Today is ' + today_date)
            elif 'who is' in command:
                person = command.replace('who is', '').strip()
                info = get_celebrity_info(person)
                print(info)
                talk(info)
            elif 'are you single' in command:
                talk('I am in a relationship with wifi')
            elif 'joke' in command:
                talk(pyjokes.get_joke())
            elif 'stock' in command:
                stock_summary = get_stock_summary()
                print(stock_summary)
                talk(stock_summary)
            elif 'who is the author of book' in command:
                book_name = command.replace('who is the author of book', '').strip()
                author_info = get_author_info(book_name)
                print(author_info)
                talk(author_info)
            else:
                talk('Please say the command again.')
        else:
            print("No command captured.")

run_sam()

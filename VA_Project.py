# Importing required packages
import speech_recognition as sr 
from gtts import gTTS
import os 
import playsound 
import wolframalpha 
from selenium import webdriver 

# Initialize global variables
num = 1
app_id = "YOUR_WOLFRAMALPHA_APP_ID"

# Function to speak output
def assistant_speaks(output):
    global num

    num += 1
    print("PerSon : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    file = str(num) + ".mp3"
    toSpeak.save(file)
    
    playsound.playsound(file, True) 
    os.remove(file)

# Function to get audio input from user
def get_audio():
    rObject = sr.Recognizer()
    audio = ''
    
    with sr.Microphone() as source:
        print("Speak...")
        audio = rObject.listen(source, phrase_time_limit=5) 
    print("Stop.")

    try:
        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text
    except:
        assistant_speaks("Could not understand your audio, Please try again!")
        return ''

# Function to process user input
def process_text(input_text):
    try:
        if 'search' in input_text or 'play' in input_text:
            search_web(input_text)
        elif "who are you" in input_text or "define yourself" in input_text:
            assistant_speaks("Hello, I am Person. Your personal Assistant. I am here to make your life easier.")
        elif "who made you" in input_text or "created you" in input_text:
            assistant_speaks("I have been created by Sheetansh Kumar.")
        elif "geeksforgeeks" in input_text:
            assistant_speaks("Geeks for Geeks is the Best Online Coding Platform for learning.")
        elif "calculate" in input_text.lower():
            calculate(input_text)
        elif 'open' in input_text:
            open_application(input_text.lower()) 
        else:
            assistant_speaks("I can search the web for you, Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input_text)
    except Exception as e:
        print(e)
        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input_text)

# Function to search the web based on user input
def search_web(input_text):
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if 'youtube' in input_text.lower():
        assistant_speaks("Opening in youtube")
        query = input_text.split('youtube')[-1].strip()
        driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query.split()))
    elif 'wikipedia' in input_text.lower():
        assistant_speaks("Opening Wikipedia")
        query = input_text.split('wikipedia')[-1].strip()
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query.split()))
    else:
        if 'google' in input_text.lower() or 'search' in input_text.lower():
            query = input_text.split('google')[-1].strip() if 'google' in input_text.lower() else input_text.split('search')[-1].strip()
            driver.get("https://www.google.com/search?q=" + '+'.join(query.split()))
        else:
            driver.get("https://www.google.com/search?q=" + '+'.join(input_text.split()))

# Function to calculate using WolframAlpha
def calculate(input_text):
    client = wolframalpha.Client(app_id)
    query = input_text.split('calculate')[-1].strip()
    res = client.query(query)
    answer = next(res.results).text
    assistant_speaks("The answer is " + answer)

# Function to open applications
def open_application(input_text):
    if "chrome" in input_text:
        assistant_speaks("Google Chrome")
        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    elif "firefox" in input_text or "mozilla" in input_text:
        assistant_speaks("Opening Mozilla Firefox")
        os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')
    elif "word" in input_text:
        assistant_speaks("Opening Microsoft Word")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Word 2013.lnk')
    elif "excel" in input_text:
        assistant_speaks("Opening Microsoft Excel")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
    else:
        assistant_speaks("Application not available")

# Main function
if __name__ == "__main__":
    assistant_speaks("What's your name, Human?")
    name = get_audio()
    assistant_speaks("Hello, " + name + '.')

    while True:
        assistant_speaks("What can I do for you?")
        text = get_audio().lower()

        if "exit" in text or "bye" in text or "sleep" in text:
            assistant_speaks("Ok bye, " + name + '.')
            break
        process_text(text)

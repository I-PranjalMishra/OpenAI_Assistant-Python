import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import openai
from config import email, password, receiver_email_id, vs_code_path, music_file_path, apikey

# FOR VOICE

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[0].id)

# FOR SPEAKING

def speak(audio):
    engine.say(audio) 
    engine.runAndWait() #Without this command, speech will not be audible to us.
    
    
# Assistant Wishing the User
    
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hello Sir. Please tell me how may I help you")  


# Taking Microphone Input and Return String


def takeCommand():     
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)  
        
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n") 

    except Exception as e:
        print("Say that again please...")   
        return "None" 
    return query      


# To Send Mail

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password) # enter your email id and its password for smtp
    server.sendmail(email, to, content) # enter your email id
    server.close()


# Chat with OpenAI using API   (To access it use your openai API)

chatStr =""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Pranjal: {query}\n My Assistant: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
   
    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

# To get answer for any prompt by OpenAI, New file will create in Answer Folder in which answer is written.
    
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    text += response["choices"][0]["text"]
    if not os.path.exists("Answer"):
        os.mkdir("Answer")

    
    with open(f"Answer/{''.join(prompt.split('intelligence')[1:10]).strip() }.txt", "w") as f:
        f.write(text)
        speak(text)
        
        
        
# MAIN Function
    
    
if __name__ == "__main__":
    wishMe()
    
    # executing tasks based on query
    
    while True:
        query = takeCommand().lower() 

        # Search on wikipedia and speak
        
        if 'from wikipedia' in query: 
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            speak(results)
            
            
        # Open any website on webbrowser (You can add any number of sites)
        
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])    
        
        # To Play Music
        
        if "play music".lower() in query:
            os.startfile(music_file_path) # put the path for the file        
        
        # To Get Time
        
        elif "time".lower() in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speak(f"Sir time is {hour} hours {min} minutes")    
         
        # Open VS Code Application
            
        elif "open vs code".lower() in query: 
            os.startfile(vs_code_path)  # put the path for the file
        
        # To Send Email Using Gmail
            
        elif 'email to Pranjal'.lower() in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = receiver_email_id   # write a mail id of the receiver or can create dictionary for more mail id's
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir. I am not able to send this email")        
        
        
        elif 'Using AI'.lower() in query.lower():
            ai(query)
            
        # To Reset The Chat
             
        elif "reset chat".lower() in query.lower():
            chatStr = ""  
            
        # To Quit
         
        elif "Quit".lower() in query.lower():
            exit()        
        
         
        # To Chat with OpenAI remove else from comment and add your OpenAI API above in chat function
            
        # else:
        #     print("Talking...")
        #     chat(query)    
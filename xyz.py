import speech_recognition as sr
from gtts import gTTS
import transformers
import os
import time
import datetime
import numpy as np

class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name
        self.capitals = {
            'france': 'paris',
            'germany': 'berlin',
            'italy': 'rome',
            'spain': 'madrid',
            'united kingdom': 'london',
            'canada': 'ottawa',
            'japan': 'tokyo',
            'australia': 'canberra',
            'india': 'new delhi',
            'china': 'beijing',
            'russia': 'moscow'
        }
    
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("Listening...")
            audio = recognizer.listen(mic)
            self.text = "ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        print("Dev --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start res.mp3')  # if you are using mac->afplay or else for windows->start
        time.sleep(int(50 * duration))
        os.remove("res.mp3")

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')

    def calculate(self, expression):
        try:
            result = eval(expression)
            return f"The result is {result}"
        except:
            return "Sorry, I couldn't calculate that."

    def get_capital(self, country):
        country = country.lower()
        if country in self.capitals:
            return f"The capital of {country.title()} is {self.capitals[country].title()}."
        else:
            return "Sorry, I don't know the capital of that country."

# Running the AI
if __name__ == "__main__":
    ai = ChatBot(name="dev")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex = True
    while ex:
        ai.speech_to_text()
        ## wake up
        if ai.wake_up(ai.text):
            res = "Hello I am Dev the AI, what can I do for you?"
        ## action time
        elif "time" in ai.text:
            res = ai.action_time()
        ## respond politely
        elif any(i in ai.text for i in ["thank", "thanks"]):
            res = np.random.choice(["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "mention not"])
        elif any(i in ai.text for i in ["exit", "close"]):
            res = np.random.choice(["Tata", "Have a good day", "Bye", "Goodbye", "Hope to meet soon", "peace out!"])
            ex = False
        ## calculate
        elif "calculate" in ai.text or "what is" in ai.text:
            expression = ai.text.lower().replace("calculate", "").replace("what is", "").strip()
            res = ai.calculate(expression)
        ## get capital
        elif "capital of" in ai.text:
            country = ai.text.lower().replace("what is the capital of", "").replace("capital of", "").strip()
            res = ai.get_capital(country)
        ## conversation
        else:
            if ai.text == "ERROR":
                res = "Sorry, come again?"
            else:
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ") + 6:].strip()
        ai.text_to_speech(res)
    print("----- Closing down Dev -----")

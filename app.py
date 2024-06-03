import tkinter as tk
from tkinter import scrolledtext
# from threading import Thread
import speech_recognition as sr
import requests
import distutils


class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
        
        self.entry_label = tk.Label(root, text="Enter your message:")
        self.entry_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.user_input = tk.Entry(root, width=30)
        self.user_input.grid(row=1, column=1, padx=10, pady=10)
        
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=2, padx=10, pady=10)
        
        self.listen_button = tk.Button(root, text="Listen", command=self.listen)
        self.listen_button.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
        
    def send_message(self):
        message = self.user_input.get()
        self.user_input.delete(0, tk.END)
        self.update_chat_display(f"You: {message}")
        response = self.send_to_backend(message)
        self.update_chat_display(f"Bot: {response}")
        
    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        try:
            message = recognizer.recognize_google(audio)
            self.user_input.delete(0, tk.END)
            self.user_input.insert(0, message)
            response = self.send_to_backend(message)
            self.update_chat_display(f"Bot: {response}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    
    def send_to_backend(self, message):
        # Assuming the backend server is running locally on port 5000
        url = "http://localhost:5000/chat"
        data = {"message": message}
        response = requests.post(url, json=data)
        return response.json()["response"]
        
    def update_chat_display(self, message):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

class ChatBot:
    def __init__(self, name):
        self.name = name
    
    def respond(self, message):
        # Placeholder for actual response generation
        return f"Bot: Hello, you said '{message}'"

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()

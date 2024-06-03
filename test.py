import speech_recognition as sr
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something:")
    audio = recognizer.listen(source)
    try:
        recognized_text = recognizer.recognize_google(audio)
        print(f"I heard you say: {recognized_text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Recog Error: {e}")

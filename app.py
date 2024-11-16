import google.generativeai as genai
from api_key import secret_key
import speech_recognition as sr
import pyttsx3

#fetching the query result from gemini model
def get_query_result(query):
    genai.configure(api_key = secret_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    chat = model.start_chat(
        history = [
            {"role":"user", "parts":"Hello"},
            {"role":"model", "parts": "Great to meet you. What would you like to know?"}
        ]
    )

    response = chat.send_message(query)

    return response.text

#converting the input to text
def speech_to_text():
    r = sr.Recognizer()
    r.pause_threshold = 3
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic, duration = 1.0) #recognizes the background noise and then takes the input
        print("Listening...")
        audio = r.listen(mic,timeout = 5,phrase_time_limit=5)    #timeout used to listen until a word is heard
        print("time over")
    
    try:
        return r.recognize_google(audio)    #the input audio will be converted to text by google's recognizer
    except:
        return "couldn't understand speak again"

#the query result will be converted to audio
def text_to_speech(query_result):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') #getting total voices available
    # print(voices)
    engine.setProperty('voice',voices[1].id) # only two voices are there so using the second voice
    engine.say(query_result)
    engine.runAndWait()

# print(chat.history)
if __name__ == "__main__":
    while True:
        query = speech_to_text().lower()
        print("You said :", query)
        if query != "" and ("bye" in query.split() or "quit" in query.split() or "stop" in query.split()):
            print("Ok Bye")
            break

        # if query == "":
        #     print("no query")
        #     continue
        query_result = get_query_result(query)
        print(query_result)
        text_to_speech(query_result)
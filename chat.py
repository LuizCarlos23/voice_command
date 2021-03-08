import speech_recognition as sr
from gtts import gTTS
from playsound  import playsound
import time
import keyboard
import webbrowser
import os

from clima import get_temperature

commands = ["pesquisar", "temperatura"]

def youtube_search(query):
    webbrowser.open("https://www.youtube.com/results?search_query="+query , new=0, autoraise=True)



def search_for_command(string):
    firt_word = string.split(' ')[0].lower()
    if (firt_word in commands):
        if (firt_word == "pesquisar"):
            youtube_search(string[10:])
        if (firt_word == "temperatura"):
            create_voice("Buscando")
            temperature = get_temperature()
            text = f"Está fazendo {temperature} graus celsius"
            create_voice(text)

def ouvir_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Microfone...")
        audio = microfone.listen(source)
    try:
        frase = microfone.recognize_google(audio,  language='pt-br')
        print("Frase: "+frase)
        return frase
    except:
        print("Deu merda aqui!!")
        return None

def create_voice(text):
    tts = gTTS(text, lang='pt-br')
    tts.save('bot.mp3')
    playsound('bot.mp3')
    os.remove('bot.mp3')

while True:
    keyboard.wait('alt+/')
    frase = ouvir_microfone()
    # print("Clicou ae vacilão")
    search_for_command(frase)

import os
import keyboard
import time
import _thread
# from multiprocessing import Process, Lock

import speech_recognition as sr
from gtts import gTTS
from playsound  import playsound
import webbrowser


from clima import fetch_current_temperature


commands = ["pesquisar no youtube", "temperatura de hoje", "pesquisar no google"]
number_of_process = 0


def youtube_search(query):
    global number_of_process
    webbrowser.open("https://www.youtube.com/results?search_query="+query , new=0, autoraise=True)
    
def google_search(query):
    global number_of_process
    webbrowser.open("https://www.google.com/search?q="+query, new=0, autoraise=True)
    


process_get_temperature = True # True: Liberado; False: Fechado
def get_temperature():
    global process_get_temperature, number_of_process
    process_get_temperature = False # Bloqueia o processo
    try:
        create_voice("Buscando")
        temperature = fetch_current_temperature()
        print("Temperatura", temperature)
        if (temperature == "error" or temperature == " "): raise
        text = f"Está fazendo {temperature} graus celsius"
        _thread.Lock.acquire
        create_voice(text)
    except Exception as e:
        create_voice("Erro na busca")
    finally:
        process_get_temperature = True # Libera o processo para ser usado
        number_of_process -= 1
        return None

def query_format(string, split_point):
    query_divided = string.split(split_point)
    del(query_divided[0])
    query = ""
    for item in query_divided:
        query += item
    print("Query: ", query)
    return query

def search_for_command(string):
    global number_of_process
    string = string.lower()
    first_word = string.split(' ')[0]
    second_word = string.split(' ')[1]
    third_word = string.split(' ')[2]
    
    first_tree_word = f"{first_word} {second_word} {third_word}"
    print("Command: ", first_tree_word)
    # command = string.split(' ')[0]
    if (first_tree_word in commands):
        if ((first_tree_word == "pesquisar no youtube") and (number_of_process != 2) ):
            query = query_format(string, "youtube")
            youtube_search(query)
        if ((first_tree_word == "pesquisar no google")):
            query = query_format(string, "google")
            number_of_process += 1
            google_search(query)
        if (first_tree_word == "temperatura de hoje"):
            if ((process_get_temperature == True) and (number_of_process != 2)):
                
                _thread.start_new_thread(get_temperature, ())
                time.sleep(.5)
                
                number_of_process += 1
            else:
                create_voice("Aguarde")
        time.sleep(0.5)
    return



def ouvir_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Microfone...")
        audio = microfone.listen(source)
    try:
        phrase = microfone.recognize_google(audio,  language='pt-br')
        print("Frase: "+phrase)
        return phrase
    except:
        print("Deu merda aqui!!")
        return None

def create_voice(text):
    tts = gTTS(text, lang='pt-br')
    tts.save('bot.mp3')
    playsound('bot.mp3')
    os.remove('bot.mp3')


def init():
    while True:
        keyboard.wait('alt+/')
        frase = ouvir_microfone()
        search_for_command(frase)

init()

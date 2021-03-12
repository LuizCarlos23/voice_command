import os
import keyboard
# from pynput import keyboard
import time
import _thread
import json
import logging
from random import choice

import speech_recognition as sr
from gtts import gTTS
from playsound  import playsound
import webbrowser


from clima import fetch_current_temperature


commands = ["pesquisar no youtube", "temperatura de hoje", "pesquisar no google", "executar"]
confirmation_text = ["Ok", "Beleza", "Certo", "Um instante"]
number_of_process = 0

logging.basicConfig(filename='bot.log', format='%(levelname)s: %(message)s', filemode='w', level=logging.DEBUG)

def youtube_search(query):
    webbrowser.open("https://www.youtube.com/results?search_query="+query , new=0, autoraise=True)
    
def google_search(query):
    webbrowser.open("https://www.google.com/search?q="+query, new=0, autoraise=True)
    
def run_program(program_name):
    with open('executable_programs.json', 'r') as json_file:
        data = json.load(json_file)
        
    program_path = data[program_name][0]
    executable_name = data[program_name][1]
    logging.info('cd %s && start %s', program_path, executable_name)
    os.system(f'cd "{program_path}" && start {executable_name}')
    os.system("cd " + os.getcwd())

process_get_temperature = True # True: Liberado; False: Fechado
def get_temperature():
    global process_get_temperature, number_of_process
    process_get_temperature = False # Bloqueia o processo
    try:
        create_voice("Buscando")
        temperature = fetch_current_temperature()
        logging.info("Temperatura: %s", temperature)
        if (temperature == "error" or temperature == " "): raise
        text = f"Está fazendo {temperature} graus celsius"
        create_voice(text)
    except Exception as e:
        create_voice("Erro na busca")
        logging.error("Error na busca da temperatura")
        logging.error("%s", e)
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
    logging.info("Query: %s", query)
    
    
    return query.strip()

def search_for_command(string):
    string = string.lower()
    
    string_divided = string.split(" ")
    
    firt_words = ""
    for word in string_divided: # Junta as "primeiraa palavras". Limite é as 3 primeiras
        if (string_divided.index(word) == 3):
            break
        elif (word in commands):
            firt_words += word
            break
        firt_words += word+" "
        
    firt_words = firt_words.strip(" ") # Eliminar espaços desnecessarios   
    
    logging.info("Command: %s ; %s", firt_words, firt_words in commands)
    
    if (firt_words in commands): call_command_functions(firt_words, string)
        


def call_command_functions(command, string ):
    try:
        global number_of_process
        random_confirmation_text = choice(confirmation_text)
        create_voice(random_confirmation_text)
        if ((command == "pesquisar no youtube")):
            query = query_format(string, "youtube")
            if (query == ""): return 
            youtube_search(query)
            
        elif ((command == "pesquisar no google")):
            query = query_format(string, "google")
            if (query == ""): return 
            google_search(query)
            
        elif (command == "temperatura de hoje"):
            if ((process_get_temperature == True) and (number_of_process != 2)):
                _thread.start_new_thread(get_temperature, ())
                time.sleep(.5)
                
                number_of_process += 1
            else:
                create_voice("Aguarde")
                
        elif (command == "executar"):
            program = query_format(string, "executar")
            run_program(program)
                
    except Exception as e:
        logging.error("Erro na call_command_functions")
        logging.error("%s", e)
    finally:
        time.sleep(0.5)
        return


def listen_to_microphone():
    microfone = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            microfone.adjust_for_ambient_noise(source)
            print("Microfone...")
            audio = microfone.listen(source, timeout=2)
            if (not audio): raise
    
        phrase = microfone.recognize_google(audio,  language='pt-br')
        print(phrase)
        logging.info("Frase: %s", phrase)
        return phrase
    except Exception as e :
        logging.error("Error na funcao listen_to_microphone")
        logging.error("%s", e)
        return None

def create_voice(text):
    tts = gTTS(text, lang='pt')
    tts.save('bot.mp3')
    playsound('bot.mp3')
    os.remove('bot.mp3')

def quit_program():
    while  True:
        if (number_of_process == 0):
            create_voice("Até mais")
            quit()
    
def listen_to_command():
    phrase = listen_to_microphone()
    if (phrase != ''):
        search_for_command(phrase)

def init():
    while True:
        if keyboard.is_pressed('alt+/'):
            listen_to_command()
        elif  (keyboard.is_pressed('ctrl+alt+c')):
            quit_program()

init()
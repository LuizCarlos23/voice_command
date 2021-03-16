from random import choice
import json
import keyboard
import logging
import os
import time
import _thread

from gtts import gTTS
from playsound  import playsound
import speech_recognition as sr
import webbrowser

from clima import fetch_current_temperature

confirmation_text = ["Ok", "Beleza", "Certo", "Um instante"]
number_of_process = 0
process_get_temperature = True # True: Liberado; False: Fechado

logging.basicConfig(filename='bot.log', format='%(levelname)s: %(message)s', 
                    filemode='w', level=logging.DEBUG)

class StringSeparate:
    def __init__(self, string):
        string = string.lower()
        self.command = self.command_search(string)
        self.query = self.query_format(string, self.command)
        
    def command_search(self, string):
        commands = ["pesquisar no youtube", 
                    "temperatura de hoje", 
                    "pesquisar no google", 
                    "executar"]
    
        command = None
        for item in commands:
            if (string.startswith(item)):
                command = item
                break
            
        return command
        
    
    def query_format(self, string, split_point = ""):
        query = string.replace(split_point, "")
        query = query.strip()
        logging.info("Query: %s", query)
        
        return query
    
class CommandFunctions:
    def __init__(self, command, query = None):
        commands = { "pesquisar no youtube": self.youtube_search, 
                    "temperatura de hoje": self.get_temperature, 
                    "pesquisar no google": self.google_search, 
                    "executar": self.run_program}
        self.query = query
        
        chose_function = commands.get(command, None)
        if (not chose_function): self.error_function("chose_function")
        else: chose_function()
        
    def error_function(self, where, message = None, error = None):
        create_voice("Ocorreu um erro")
        logging.erro("Ocorreu um erro em: %s", where)
        if (message): logging.debug("%s", message)
        if (error): logging.debug("%s", error)
        
    def youtube_search(self):
        if (not self.query): return error_function("youtube_search")
        webbrowser.open("https://www.youtube.com/results?search_query="+self.query , new=0, autoraise=True)
    
    def google_search(self):
        if (not self.query): return error_function("google_search")
        webbrowser.open("https://www.google.com/search?q="+self.query, new=0, autoraise=True)
        
    def run_program(self):
        if (not self.query): return error_function("run_program")
        
        with open('executable_programs.json', 'r') as json_file:
            data = json.load(json_file)
            
        program_path = data.get(self.query, None)[0]
        executable_name = data.get(self.query, None)[1]
        
        if (program_path == None or executable_name == None):
            return error_function("run_program", f"program_path ou executable_name não encontrado (program_path:{program_path} ; executable_name:{executable_name}) ")
        elif (program_path == "shell"):
            logging.info("start %s", executable_name)
            os.system("start "+executable_name)
        else:
            logging.info('cd %s && start %s', program_path, executable_name)
            os.system(f'cd "{program_path}" && start {executable_name}')
            os.system("cd " + os.getcwd())
        return "Okay"
    
    def get_temperature(self):
        global process_get_temperature, number_of_process
        number_of_process += 1
        process_get_temperature = False # Bloqueia o processo
        try:
            create_voice("Buscando")
            temperature = fetch_current_temperature()
            logging.info("Temperatura: %s", temperature)
            if (temperature == "error" or temperature == " "): raise
            text = f"Está fazendo {temperature} graus celsius"
            create_voice(text)
        except Exception as error:
            error_function("get_temperature", "Error na busca da temperatura", error)
        finally:
            process_get_temperature = True # Libera o processo para ser usado
            number_of_process -= 1
            return None


def call_command_functions(string):
    try:
        random_confirmation_text = choice(confirmation_text)
        create_voice(random_confirmation_text)
        
        string_separete_result = CommandFunctions(string)
        query = string_separete_result.query
        command = string_separete_result.command
        if (command == None or query == None): return
        CommandFunctions(command, query)
    except Exception as e:
        logging.error("Erro na call_command_functions")
        logging.error("%s", e)
    finally:
        time.sleep(0.5)
        return


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

   
def listen_to_microphone():
    microfone = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            microfone.adjust_for_ambient_noise(source)
            print("Microfone...")
            create_voice("Escutando")
            audio = microfone.listen(source, timeout=3)
            if (not audio): raise
    
        phrase = microfone.recognize_google(audio,  language='pt-br')
        print(phrase)
        logging.info("Frase: %s", phrase)
        return phrase
    except Exception as e :
        logging.error("Error na funcao listen_to_microphone")
        logging.error("%s", e)
        return None    


def init():
    create_voice("Estou a disposição")
    while True:
        if keyboard.is_pressed('alt+/'):
            phrase = listen_to_microphone()
            if (phrase != None): call_command_functions(phrase)
            
        elif  (keyboard.is_pressed('ctrl+alt+c')):
            quit_program()

init()
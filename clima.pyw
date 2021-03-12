# ------------------------Algoritmo Temporario-------------------------------------
# Busca temperatura usado o selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import time
import logging
logging.basicConfig(filename='bot.log', format='%(levelname)s: %(message)s',level=logging.DEBUG)

url = "https://www.msn.com/pt-br/clima"
option = Options()
option.headless = True
def fetch_current_temperature():
    logging.info("Executou a função fetch_current_temperature")
    driver = webdriver.Firefox(options=option)
    driver.get(url)
    time.sleep(3)
    try:
        element = driver.find_element_by_css_selector("span.temperature-DS-EntryPoint1-1")
        html_content = element.get_attribute('outerHTML')
        soup = bs(html_content, 'html.parser')
        temperatura = soup.text.replace("°", " ")
        driver.close()
        return temperatura
    except Exception as e:
        print(e)
        driver.close()
        return "error"

#--------------------------------------------------------------------------------

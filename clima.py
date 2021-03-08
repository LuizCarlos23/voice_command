# ------------------------Algoritmo Temporario-------------------------------------

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import time

# url = "https://www.cptec.inpe.br/previsao-tempo/ce/fortaleza"
url = "https://www.msn.com/pt-br/clima"
option = Options()
option.headless = True
def get_temperature():
    driver = webdriver.Firefox(options=option)
    driver.get(url)
    time.sleep(2)
    try:
        element = driver.find_element_by_css_selector("span.temperature-DS-EntryPoint1-1")
        html_content = element.get_attribute('outerHTML')
        soup = bs(html_content, 'html.parser')
        temperatura = soup.text[:2]
        driver.close()
        return temperatura
    except Exception as e:
        driver.close()
        return None

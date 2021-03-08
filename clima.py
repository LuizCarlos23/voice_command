# ------------------------Algoritmo Temporario-------------------------------------

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import time

url = "https://www.cptec.inpe.br/previsao-tempo/ce/fortaleza"
option = Options()
option.headless = True
def get_temperature():
    driver = webdriver.Firefox(options=option)
    driver.get(url)
    time.sleep(2)
    try:
        element = driver.find_element_by_css_selector("div.temperaturas")
        html_content = element.get_attribute('outerHTML')
        soup = bs(html_content, 'html.parser')
        html_span = soup.find_all(name='span')
        temperaturas = []
        for span in html_span:
            temperaturas.append(span.contents[0][:2])
        temperaturas = {"min": temperaturas[0], "max": temperaturas[1]}
        driver.close()
        return temperaturas
    except Exception as e:
        driver.close()
        return None

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
import random

browser = webdriver.Chrome() #это переменная которая хранит созданный экземпляр браузера., в которой хранится объект веб-драйвера Chrome, которая запускает экземпляр браузера. Этот объект позволяет вам управлять браузером(для автоматизации действий): открывать страницы, взаимодействовать с элементами, заполнять формы, щелкать по кнопкам и т. д.

browser.get('https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BB%D0%BD%D0%B5%D1%87%D0%BD%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0')
paragrafs = browser.find_elements(By.TAG_NAME, 'p')  # находим все параграфы - теги "р" это список

# for paragraf in paragrafs:
#     print(paragraf.text)
#     input()

# <div role="note" class="hatnote navigation-not-searchable ts-main"><style data-mw-deduplicate="TemplateStyles:r142002967">.mw-parser-output .ts-main a{font-weight:bold}.mw-parser-output .ts-main a.new,.mw-parser-output .ts-main a.extiw,.mw-parser-output .ts-main a.external{font-weight:normal}</style>Основная статья: <a href="/wiki/%D0%A1%D0%BE%D0%BB%D0%BD%D1%86%D0%B5" title="Солнце">Солнце</a></div>

hatnotes = []

for element in browser.find_elements(By.TAG_NAME, 'div'):
    cls = element.get_attribute('class')
    if cls == 'hatnote navigation-not-searchable ts-main':
        hatnotes.append(element)

print(hatnotes)
hatnotes = random.choice(hatnotes)
link = hatnotes.find_element(By.TAG_NAME, 'a').get_attribute('href')
browser.get(link)
time.sleep(5)

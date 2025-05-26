# Напишите программу, с помощью которой можно искать информацию на Википедии с помощью консоли.
# 1. Спрашивать у пользователя первоначальный запрос.
# 2. Переходить по первоначальному запросу в Википедии.
# 3. Предлагать пользователю три варианта действий:
# листать параграфы текущей статьи;
# перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
# выйти из программы.


# Добавьте явное ожидание (Explicit Wait)
# Используйте модуль `WebDriverWait`
from selenium.webdriver.support.ui import WebDriverWait
# и `expected_conditions`, чтобы дождаться, когда элемент станет кликабельным или доступным для взаимодействия.
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
import random

browser = webdriver.Chrome() #это переменная которая хранит созданный экземпляр браузера, в которой хранится объект веб-драйвера Chrome, которая запускает экземпляр браузера. Этот объект позволяет вам управлять браузером(для автоматизации действий): открывать страницы, взаимодействовать с элементами, заполнять формы, щелкать по кнопкам и т. д.

browser.get('https://ru.wikipedia.org/')

assert "Википедия" in browser.title #Проверяем по заголовку, тот ли сайт открылся


# Ждем, пока поле поиска станет кликабельным
wait = WebDriverWait(browser, 10)
search_box = wait.until(EC.element_to_be_clickable((By.ID, 'searchInput')))#Находим окно поиска

user_ask = input('Введите что хотите найти: - ')

# Вводим запрос
search_box.send_keys(user_ask) # Прописываем ввод текста в поисковую строку. В кавычках тот текст, который нужно ввести
search_box.send_keys(Keys.RETURN)#Добавляем не только введение текста, но и его отправку

wait.until(EC.presence_of_element_located((By.ID, 'content')))# Ждем загрузки страницы результатов (пример)



time.sleep(5)



paragrafs = browser.find_elements(By.TAG_NAME, 'p')



# browser.quit() # Не забудьте закрыть браузер в конце
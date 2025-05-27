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
browser.get('https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0')
assert "Википедия" in browser.title #Проверяем по заголовку, тот ли сайт открылся

# Ждем, пока поле поиска станет кликабельным
wait = WebDriverWait(browser, 10)          # searchInput
# search_box = browser.find_element(By., 'simpleSearch')
search_box = wait.until(EC.element_to_be_clickable((By.ID, 'searchInput'))) # Находим окно поиска

user_ask = input('Введите что хотите найти: - ')


# Вводим запрос
search_box.send_keys(user_ask) # Прописываем ввод текста в поисковую строку. В кавычках тот текст, который нужно ввести
search_box.send_keys(Keys.RETURN)#Добавляем не только введение текста, но и его отправку
wait.until(EC.presence_of_element_located((By.ID, 'content')))# Ждем загрузки страницы результатов (пример)

time.sleep(5)
print()


user_ask = input('Вы хотите: '
                 '\nПолучить и пролистать параграфы этой статьи (страници) (1) '
                 '\nПерейти на одну из связанных страниц (2)'
                 '\nВыйти из программы (3)   Итак: - ')
# print()
print(user_ask)




if user_ask == '1': # Получить и пролистать параграфы этой статьи (страници)
    # class ="mw-search-result mw-search-result-ns-0 searchresult-with-quickview"
    hatnotes = []

    for element in browser.find_elements(By.TAG_NAME, 'li'):
        cls_ = element.get_attribute('class')
        # print('cls_^',cls_)
        if cls_ == 'mw-search-result mw-search-result-ns-0 searchresult-with-quickview': # "mw-search-result mw-search-result-ns-0 searchresult-with-quickview"
            print("На этой странице нет параграфов, есть только заголовки, вот они. Нажмите Enter, чтобы продолжить")
            hatnotes.append(element)
            word = element.get_attribute('data-prefixedtext')
            print( word)
            input()
    print('hatnotes',hatnotes)
    paragrafs = browser.find_elements(By.TAG_NAME, 'p') # находим все параграфы - теги "р" это список



    for paragraf in paragrafs:
        print("А вот вам и параграф. Сорри, какой есть. Нажмите Enter, чтобы продолжить")
        print(paragraf.text)
        input()





elif user_ask == '2':  # Перейти на одну из связанных страниц (2)

    hatnotes = []
    for element in browser.find_elements(By.TAG_NAME, 'li'):
        cls_ = element.get_attribute('class')
        # print('cls_^',cls_)
        if cls_ == 'mw-search-result mw-search-result-ns-0 searchresult-with-quickview':  # "mw-search-result mw-search-result-ns-0 searchresult-with-quickview"
            hatnotes.append(element)
            word = element.get_attribute('data-prefixedtext')
            # print(word)
    # print('hatnotes', hatnotes)
    hatnote = random.choice(hatnotes)
    link = hatnote.find_element(By.TAG_NAME, 'a').get_attribute('href')
    browser.get(link)

    user_ask2 = input('\nВы хотите: \nЛистать параграфы статьи (1), \nПерейти на одну из внутренних статей (2). Итак: - ')
    print(user_ask2)


    if user_ask2 == '1': # Листать параграфы статьи
        print('Листаем параграфы статьи')
        paragrafs = browser.find_elements(By.TAG_NAME, 'p')  # находим все параграфы - теги "р" это список
        for paragraf in paragrafs: # Листаем параграфы
            print(paragraf.text)
            input()

    elif user_ask2 == '2': # Перейти на одну из внутренних статей
        print()
        print(' Переходим по внутренним ссылкам которых в статье:')

        container = browser.find_element(By.ID, "mw-content-text") # Находим контейнер

        # Находим все li внутри контейнера с нужными классами  "li.toclevel-1"
        li_elements = container.find_elements(By.CSS_SELECTOR,
                                              'li.toclevel-1') # все
        print(' Всего',len(li_elements), 'шт')

        random_li = random.choice(li_elements) # Выбираем случайный li

        link = random_li.find_element(By.TAG_NAME, 'a') # Находим ссылку внутри выбранного li

        # Переходим по ссылке
        link_href = link.get_attribute('href')
        browser.get(link_href)
        time.sleep(15)



elif user_ask == '3': # Выйти из программы
    print('Выходим...')
    exit()






# browser.quit() # Не забудьте закрыть браузер в конце
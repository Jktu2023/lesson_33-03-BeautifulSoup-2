from googletrans import Translator
import requests
from bs4 import BeautifulSoup


url = 'https://randomword.com/'

def translate(word):
    translator = Translator()
    result = translator.translate(word, dest='ru')
    # text = translator.translate('hello', dest='ja')
    return result.text

def get_random_word(): # функция парсер слова и его описания с сайта
    print(f'{url} - рулит!')
    try:
        response = requests.get(url) # получаем ответ
        if response.ok:
            print('До сервера достучались. Ok!\n')
        soup = BeautifulSoup(response.content, 'html.parser') # парсим, создаем обьект суп

        english_word = soup.find('div', id="random_word").text # находим слово в теге с ид
        print(english_word)
        word_definition = soup.find('div', id="random_word_definition").text # находим описание слова в теге с ид
        print(word_definition)

        return {
            'english_word': english_word,
            'word_definition': word_definition
        }

    except Exception as e:
        print('Что-то пошло не так, сработало исключение на ошибку:\n', e)


def game():
    print('\nИграем!')
    while True:
        word_dict = get_random_word() # парсим слово и описание с сайта и помещаем с словарь
        english_word = word_dict['english_word'] # значение по ключу из словаря 1м способом
        english_word_definition = word_dict.get('word_definition')  # значение по ключу из словаря 2м способом
        russian_word = translate(english_word) # переводим
        russian_word_definition = translate(english_word_definition) # переводим

        user_say = input(f'Посмотрите описание ({russian_word_definition}) и введите слово которое ему соответствует: - ')
        if user_say == russian_word:
            print('Ответ правильный!')
        else:
            print(f'Ответ не правильный! Это слово {russian_word}, ({english_word}).')

        play_again = input('Попробуете еще раз? (y/n): - ')
        if play_again == 'n':
            print('Игра сделана!')
            break

game()






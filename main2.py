from telebot import TeleBot, types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message, Chat
from test import TOKEN

bot = TeleBot(TOKEN)
file_path = 'C:/Users/Anaconda/PycharmProjects/Zerocoder/dist/listbox_contents.txt' # указываем файл с данными и путь)
bot.state = {}  # словарь нициализации состояния бота
def load_file(): # загружает значения из файла listbox_contents.txt,
    print(file_path)
    if file_path:  # если он коректно указан
        list_box = [] # создаем список перед загрузкой нового содержимого
        with open(file_path, 'r', encoding='cp1251', errors='ignore') as file:# Открываем файл и читаем его содержимое
            for line in file:
                list_box.append(line.strip())   # Добавляем строку в Listbox
    return list_box # возвращаем заполненый из файла список

def save_file(items):  # Функция для сохранения списка в файл
    with open(file_path, 'w', encoding='cp1251') as file:
        for item in items:
            file.write(item + '\n')  # Записываем каждый элемент в новую строку (f"{item}\n")

def simulate_start_command(chat_id): # Функция для имитации вызова команды /start
    # Создаем объект сообщения с необходимыми атрибутами
    message = Message()
    message.chat = Chat(id=chat_id)  # Устанавливаем ID чата
    message.text = "/start"  # Устанавливаем текст сообщения

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    items = load_file() # присваеваем пременной список, загруженый из файла
    # отправка ответа на сообщение пользователя 'start', 'help'.
    bot.reply_to(message, 'Привет! Я ТГ-бот, я буду помогать тебе с твоими задачами и целями! \nУдалять выполненые и ставить новые')
    # создаётся объект класса`ReplyKeyboardMarkup`, который используется для создания пользовательской клавиатуры
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎯 Добавить задачу"))  # Добавляем кнопку для добавления новой задачи. Добавляем кнопку с эмодзи➕
    for item in items: # перебор элементов списка
        markup.add(KeyboardButton(item)) # создаются кнопки в виде элементов списка
    # отправка сообщения в чат
    bot.send_message(message.chat.id, "Выберите решенную задачу и ее можно будет удалить. Либо добавьте новую:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    items = load_file()  # присваиваем переменной список, загруженный из файла

    if message.text in items:  # Если выбрана задача для удаления  # например:   items: ['Досмотреть видео по Jango', 'Посмотреть книгу по Jango', 'Сделать Anki по Tkinter', 'Посмотреть допзанятие по парсингу и Pandas', 'Посмотреть видео о Linux и парсингу']
        # Запрашиваем подтверждение удаления, создается клавиатура ДА - НЕТ на месте предпредшествующей клавы
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
        bot.send_message(message.chat.id, f'Вы выбрали: {message.text}. Вы уверены, что хотите удалить эту задачу?',
                         reply_markup=markup)
        bot.last_selected_item = message.text  # Сохраняем выбранный ответ в атрибуте

    elif message.text == "Да":  # если выбрал по кнопке ДА - удаляем из списка
        if hasattr(bot, 'last_selected_item'):  # если мы получили в бот атрибут 'last_selected_item'
            item_to_remove = bot.last_selected_item # присваеваем его имя пременной
            items.remove(item_to_remove) # и удаляем этот элемент из списка items
            bot.send_message(message.chat.id, f'Была удалена задача: "{item_to_remove}".') # оптавляем об этом сообщение в чат-бот
            del bot.last_selected_item # Удаляем после этого и сам атрибут после использования, очищаеи поле атрибуда для дальнейшей работы
            save_file(items)  # Сохраняем изменения в файл
            send_welcome(message)  # Обновляем список задач в боте через сообщение

    elif message.text == "🎯 Добавить задачу":  # Обработка нажатия кнопки "Добавить задачу"
        print("bot.state:", bot.state)
        bot.send_message(message.chat.id, "Введите описание новой задачи:")
        bot.state[message.from_user.id] = "waiting_for_task"  # Устанавливаем состояние ожидания новой задачи

    elif message.from_user.id in bot.state and bot.state[message.from_user.id] == "waiting_for_task":
        print("bot.state:", bot.state)
        new_task = message.text
        items.append(new_task)  # Добавляем новую задачу в список
        save_file(items)  # Сохраняем изменения в файл
        bot.send_message(message.chat.id, f'Задача "{new_task}" добавлена.')  # Подтверждение добавления
        del bot.state[message.from_user.id]  # Удаляем состояние после добавления
        send_welcome(message)  # Обновляем список задач в боте через сообщение

bot.polling(none_stop=True)# Запускает бота, постоянно опрашивая серверы Telegram на предмет новых сообщений.
# Не забудьте добавить обработчик для запуска бота


#
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     items = load_file()  # присваиваем переменной список, загруженный из файла
#     # print('message.text:', message.text)
#     #print('items:', items)
#
#     if message.text in items:  # Если выбрана задача для удаления
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
#         bot.send_message(message.chat.id, f'Вы выбрали: {message.text}. Вы уверены, что хотите удалить эту задачу?',
#                          reply_markup=markup)
#         bot.last_selected_item = message.text  # Сохраняем выбранный ответ в атрибуте
#
#     elif message.text == "Да":  # # если выбрал по кнопек ДА - удаляем из списка
#         if hasattr(bot, 'last_selected_item'):  # если мы получили в бот атрибут 'last_selected_item'
#             item_to_remove = bot.last_selected_item
#             items.remove(item_to_remove)
#             bot.send_message(message.chat.id, f'Была удалена задача: "{item_to_remove}".')
#             del bot.last_selected_item
#             save_file(items)  # Сохраняем изменения в файл
#             send_welcome(message)  # Обновляем список задач в боте
#
#     elif message.text == "Добавить задачу":  # Обработка нажатия кнопки "Добавить задачу"
#         bot.send_message(message.chat.id, "Введите описание новой задачи:")
#         bot.set_state(message.from_user.id, "waiting_for_task")  # Устанавливаем состояние ожидания новой задачи
#         print('hasattr(bot, state):', hasattr(bot, 'state'))
#         print('bot.state.get(message.from_user.id):', bot.state.get(message.from_user.id))
#
#
#     elif hasattr(bot, 'state') and bot.state.get(message.from_user.id) == "waiting_for_task":
#         new_task = message.text
#         items.append(new_task)  # Добавляем новую задачу в список
#         print('new_task:', new_task)
#         print('items:', items)
#         save_file(items)  # Сохраняем изменения в файл
#         bot.send_message(message.chat.id, f'Задача "{new_task}" добавлена.')  # Подтверждение добавления
#         del bot.state[message.from_user.id]  # Удаляем состояние после добавления




# @bot.message_handler(func=lambda message: True)
# def handle_message(message): # message.text: Досмотреть видео по Jango - то что выбрал тользователь с виртуальной клавиатуры
#     items = load_file()  # присваеваем пременной список, загруженый из файла
#     print('message.text:',message.text)
#     print('items:', items)
#     if message.text in items: # например:   items: ['Досмотреть видео по Jango', 'Посмотреть книгу по Jango', 'Сделать Anki по Tkinter', 'Посмотреть допзанятие по парсингу и Pandas', 'Посмотреть видео о Linux и парсингу']
#         # Запрашиваем подтверждение удаления, создается клавиатура ДА - НЕТ на месте предидущей клавы
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
#         bot.send_message(message.chat.id, f'Вы выбрали: {message.text}. Вы уверены, что хотите удалить эту задачу?',
#                          reply_markup=markup)
#
#         # Сохраняем выбранный ответ в атрибуте для дальнейшего использования
#         bot.last_selected_item = message.text # message.text: Досмотреть видео по Jango - то что выбрал тользователь с виртуальной клавиатуры
#     elif message.text == "Да": # если он выбрал ДА - удаляем из списка
#         if hasattr(bot, 'last_selected_item'): # если мы получили в бот атрибут 'last_selected_item'
#             item_to_remove = bot.last_selected_item # присваеваем его имя пременной
#             items.remove(item_to_remove) # и удаляем этот элемент из списка items
#             bot.send_message(message.chat.id, f'Была удалена задача: "{item_to_remove}".') # оптавляем об этом информацию в чат-бот
#             del bot.last_selected_item  # Удаляем после этого и сам атрибут после использования, очишаеи поле атрибуда для дальнейшей работы
#             send_welcome(message)  # Обновляем список задач в боте через сообщение
#             print('message:', message)
#
#             with open(file_path, 'w', encoding='cp1251') as file:
#                 for item in items:
#                     file.write(item + '\n')  # Записываем каждый элемент в новую строку
#
#         else: # если атрибут отсутствует - отправляем в чат сообщение:
#             bot.send_message(message.chat.id, 'Нет выбранной задачи для удаления.')
#     elif message.text == "Нет": # если он выбрал НЕТ - отправляем в чат сообщение:
#         bot.send_message(message.chat.id, 'Удаление отменено.')
#     else: # в остальных случаях - отправляем в чат сообщение:
#         bot.send_message(message.chat.id, 'Пожалуйста, выберите задачу из списка для удаления.')
#         send_welcome(message) # Вызываем обработчик для отправки "/start" в чат-бот (авто-обновления списка задач)




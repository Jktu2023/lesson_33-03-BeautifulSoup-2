import telebot
import datetime
import time
import threading
import random

bot = telebot.TeleBot('7713027782:AAGKMkfIN2DstaYaqNTpfrNfUXYbkCY4FX4') # идентификация пином переменной с ботом

list_ = [' ** Человек на 90% состоит из воды. **',
        ' ** В день нужно выпивать 1л воды. **',
        ' ** Желательно, что бы вода была не кипяченой, а просто теплой. **',
        ' ** Пейте теплую воду одельными глотками - и не часто, ладони держите в области почек, прогревая почки. **',
        ' ** Если вы голодаете, обязательно нужно пить воду - очищение происхолит эффективнее, если конечно, голодание не сухое. **',
        ' ** Если выпивать воду в нужном количестве, из организма выводятся шлаки. **']

@bot.message_handler(commands=['start']) #декоратор хэндлер
def start_message(messsge):
    bot.reply_to(messsge, 'Привет! Я ТГ-бот, я буду напоминать тебе пить водичку, и делать это во время!') #Является способом отправки ответа на сообщение пользователя.
    rem_thread = threading.Thread(target=send_rem, args=(messsge.chat.id,))
    rem_thread.start()

@bot.message_handler(commands=['fact']) #декоратор хэндлер
def fact_message(message):
    print(message)

    waters_fact = random.choice(list_)
    bot.reply_to(message, f'Факт о воде: {waters_fact}') #Является способом отправки ответа на сообщение пользователя.

def send_rem(chat_id):
    rem_times = [
        '09:00',
        '12:00',
        '15:00',
        '17:00',
        '20:00']

    while True:
        now = datetime.now().strftime('%H:%M')
        if now in rem_times:
            waters_fact = random.choice(list_)
            print('chat_id:', chat_id)
            bot.send_message(chat_id, f'Напоминаю тебе, что нужно выпить стакан теплой воды!\n \n{waters_fact}')

            time.sleep(61)
        time.sleep(1)

bot.polling(none_stop=True)# Запускает бота, постоянно опрашивая серверы Telegram на предмет новых сообщений.


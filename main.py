import telebot
import requests
import json

token='6208232516:AAE6r1nAhl5r7m0GiHGurY_v9h3XppW5f54'
bot=telebot.TeleBot(token)
keys = {'евро': 'EUR', 'доллар': 'USD', 'рубль': 'RUB'}


class valException(Exception):
    pass

class cry_conv:
    @staticmethod
    def convert1(val_to, val_from, kol):
        if val_to == val_from:
            raise valException('Валюты не должны быть одинаковыми!')
        try:
            val_to1 = keys[val_to]
        except KeyError:
            raise valException(f'Не правильное название валюты {val_to}!')
        try:
            val_from1 = keys[val_from]
        except KeyError:
            raise valException('Не правильное название валюты {val_from}!')
        try:
            kol = float(kol)
        except ValueError:
            raise valException('Параметр "количество" не правильно записан: {kol}!')
        url = f"https://api.apilayer.com/currency_data/convert?to={val_to1}&from={val_from1}&amount={kol}"
        payload = {}
        headers = {"apikey": "svKCmvWwihJuXSsWXH8OrXj6ph2d1ZIm"}
        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.text
        r = result.split()
        return r[r.index('"result":') + 1]

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Вводи команды боту в следующем формате:\n\
    <название исходной валюты>  <в какую валюту переводишь>  \
    <количество исходной валюты>\n\
    Список доступных валют по команде: /values'
    bot.reply_to(message, text)  # функция отправляет ответ на конкретное сообщение

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise valException('Неверное число параметров!')
        val_to, val_from, kol = values
        cena = cry_conv.convert1(val_to, val_from, kol)
    except valException as e:
        bot.reply_to(message,f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать запрос.\n{e}')
    else:
        text = f'Цена {kol} {val_to} в {val_from} - {cena}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
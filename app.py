import telebot

import random
from config import TOKEN, keys, emoji, memes_for_exceptions, memes_for_star_message
from extensions import ConverterException, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    bot.send_message(message.chat.id, f"Для конвертирования валюты введите сообщение боту в следующем формате: \n\n<имя валюты>\
<в какую валюту перевести> <количество переводимой валюты> \n\n Например: \n евро рубль 12 \n\n /start и /help показывают \
формат ввода и основные команды бота \n /values показывает список доступных валют для конвертирования")
    bot.send_photo(message.chat.id, memes_for_star_message[random.randrange(len(memes_for_star_message))])


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    for key in keys.keys():
        text = f'\n {emoji[key] }'.join((text, key, ))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConverterException('Слишком много или недостаточно параметров \n\n Пример ввода: \n доллар рубль 1\
\n\n /start и /help показывают формат ввода и основные команды бота')

        quote, base, amount = values
        conversion_result = APIException.get_price(quote, base, amount)

    except ConverterException as e:
        bot.reply_to(message, f'{e}')
        bot.send_photo(message.chat.id, memes_for_exceptions[random.randrange(len(memes_for_exceptions))])
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n\n {e}')

    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} - {conversion_result}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

import telebot
from Config import keys, TOKEN
from Extensions import ConvertiomException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
           '/values - посмотреть список доступных валют\n' \
           '/help - инструкция по применению бота'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def welcome(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        values = list(map(str.lower, values))
        if len(values) != 3:
            raise ConvertiomException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except ConvertiomException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Переводим {quote} в {base}:\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
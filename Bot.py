# Этот бот считает пропорцию: если на 100г первого продукта приходится "х" грамм другого продукта, то сколько грамм другого продукта нужно для введенного нами нового значения первого продукта

import telebot

# Создаем экземпляр бота с указанием токена
bot = telebot.TeleBot('6988792415:AAG5AnGJbdiVuMXsUZq5q4eKI1AbnxNciKg')

# Словарь для хранения состояний пользователей
user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я могу помочь вам решить пропорцию между двумя продуктами. '
                                      'Пожалуйста, введите вес или объем каждого продукта.')


# Обработчик команды /solve
@bot.message_handler(commands=['solve'])
def solve_proportion(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'first_product'}
    bot.send_message(chat_id, 'Введите вес или объем первого продукта:')


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        step = user_data[chat_id]['step']

        try:
            value = float(message.text)

            if step == 'first_product':
                user_data[chat_id]['first_product'] = value
                user_data[chat_id]['step'] = 'first_product_weight'
                bot.send_message(chat_id, 'Введите вес или объем второго продукта:')

            elif step == 'first_product_weight':
                user_data[chat_id]['first_product_weight'] = value
                user_data[chat_id]['step'] = 'second_product_weight'
                bot.send_message(chat_id, 'Введите Ваш вес или объем продукта:')

            elif step == 'second_product_weight':
                first_product = user_data[chat_id]['first_product']
                first_product_weight = user_data[chat_id]['first_product_weight']
                second_product_weight = value

                second_product = (first_product_weight * second_product_weight) / first_product

                bot.send_message(chat_id,
                                 f'Для Вашего продукта нужно {second_product:.2f} г или мл.')
                del user_data[chat_id]

        except ValueError:
            bot.send_message(chat_id, 'Пожалуйста, введите число.')


# Запускаем бота
bot.polling()
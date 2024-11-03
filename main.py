import telebot
import validators
import requests
import re

API_TOKEN = '7855743766:AAHRBr2Iq_d0vU3bV9l18P-riSPKwwJiAmA'

bot = telebot.TeleBot(API_TOKEN)

def extract_clothing_description(text):
    match = re.search(r'wearing (.+)', text)
    if match:
        description = match.group(1)
        return description.strip()
    return ""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет мир!")


@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.send_message(message.chat.id,"It`s info!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if(validators.url(message.text)):
        bot.send_message(message.chat.id, "Ожидайте результат.")
        url = 'https://5cab-34-19-122-212.ngrok-free.app/receive'
        query = {'text': message.text, 'prompt': "<image>What clothes is the person in the photograph wearing in its main focus?<bos>"}
        response = requests.post(url, json=query)
        bot.send_message(message.chat.id, response.text)
        text = extract_clothing_description(response.text)
        
    else:
        bot.send_message(message.chat.id, "Это не ссылка! Отправьте мне ссылку!")

bot.polling()
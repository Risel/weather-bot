import telebot
from telebot import types

bot = telebot.TeleBot('6713450515:AAE-43LZ7Lc6D58JbnrnSP-koF9hU9lX39A')

def send_fuck_audio(message):
  audio = open(r'/Users/mtfild/Downloads/idi-nakhui-suka_9p27MbW.mp3', 'rb')
  bot.send_audio(message.chat.id, audio)
  audio.close()
  
def send_greeting(message): 
  last_name = message.from_user.last_name if message.from_user.last_name else ''
  greeting = f'Дарова, {message.from_user.first_name} {last_name}'.strip()
  bot.send_message(message.chat.id, f'{greeting}, пошли меня нахуй')

@bot.message_handler(commands=['start', 'main', 'hello'])

def start_message(message):
  send_greeting(message)

@bot.message_handler(commands=['help'])

def help_message(message):
  bot.send_message(message.chat.id,"<strong>Че помощь нужна?</strong>", parse_mode='html')

@bot.message_handler(commands=['fuck'])

def send_audio(message):
  send_fuck_audio(message)

@bot.message_handler()

def info(message):
  if message.text.lower() == 'привет':
    send_greeting(message)
  elif message.text.lower() == 'пошел нахуй':
    send_fuck_audio(message)
    
bot.polling(non_stop=True)
import telebot
from telebot import types
import requests


BOT_TOKEN = '6713450515:AAE-43LZ7Lc6D58JbnrnSP-koF9hU9lX39A'
WEATHER_API = 'ec1640fb5299f4bfed850744e0d1a2cf'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_greeting(message): 
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  button_geo = types.KeyboardButton(text="Отправить геолокацию", request_location=True)
  button_msk = types.KeyboardButton(text='Москва')
  button_sbp = types.KeyboardButton(text='Санкт-Петербург')
  button_ekb = types.KeyboardButton(text='Екатеринбург')
  markup.row(button_msk,button_sbp, button_ekb)
  markup.row(button_geo)
  bot.send_message(message.chat.id, "Привет! Выберите город или нажмите кнопку ниже, чтобы отправить свою геолокацию, либо введите название города.", reply_markup=markup)

def get_weather(latitude, longitude, api_key):
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=ru"
  response = requests.get(url)
  print(response.json())
  data = response.json()
  if response.status_code == 200:
      weather = data['weather'][0]['description']
      temperature = data['main']['temp']
      feels_like = data['main']['feels_like']
      return f"Погода: {weather}, Температура: {temperature}°C, ощущается как {feels_like}°C"
  else:
      return "Ошибка получения данных о погоде."
    
def get_weather_by_city(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        return f"Погода в {city_name.title()}: {weather}, Температура: {temperature}°C, Ощущается как {feels_like}°C"
    else:
        return "Ошибка получения данных о погоде. Проверьте название города."

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    city = message.text
    weather_info = get_weather_by_city(city, WEATHER_API)
    bot.send_message(message.chat.id, weather_info)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location:
        weather_info = get_weather(message.location.latitude, message.location.longitude, WEATHER_API)
        bot.send_message(message.chat.id, weather_info)  
      

bot.polling(non_stop=True)
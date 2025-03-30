import telebot, requests
import os
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Загрузка переменных из .env файла
load_dotenv()

TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('WEATHER_API_KEY')

URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'

EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀',
              801: '🌤',
              802: '☁️',
              803: '☁️',
              804: '☁️'}

bot = telebot.TeleBot(TOKEN)


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('Ввести название города'))
keyboard.add(KeyboardButton('О проекте'))


def get_weather(lat=None, lon=None, city=None):
    if city:
        params = {'q': city, 'lang': 'ru', 'units': 'metric', 'appid': API_KEY}
    else:
        params = {'lat': lat, 'lon': lon, 'lang': 'ru', 'units': 'metric', 'appid': API_KEY}
    
    try:
        response = requests.get(url=URL_WEATHER_API, params=params).json()
        
        if 'cod' in response and response['cod'] == '404':
            return 'Город не найден. Пожалуйста, проверьте правильность написания.'
            
        city_name = response['name']
        description = response['weather'][0]['description']
        code = response['weather'][0]['id']
        temp = response['main']['temp']
        temp_feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']

        emoji = EMOJI_CODE[code]
        message = f'🏙️ONLY IN OHIO☠ Погода в: {city_name}\n'
        message += f'{emoji} {description.capitalize()}.\n'
        message += f'🌡️ Температура: {temp}°C.\n'
        message += f'🌡️  Ощущается {temp_feels_like}.\n'
        message += f'💧🐸 Влажность {humidity}%.\n'
        return message
    except Exception as e:
        return f'Произошла ошибка при получении данных о погоде: {str(e)}'
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
   text = 'Вы можете отправить мне своё местоположение или ввести название города, чтобы узнать погоду.'
   bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='О проекте')
def send_info(message):
    text = 'Этот бот был создан Арахисом'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='Ввести название города')
def ask_city(message):
    text = 'Введите название города:'
    sent = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent, process_city_step)

def process_city_step(message):
    city = message.text
    result = get_weather(city=city)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat=lat, lon=lon)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)

bot.infinity_polling()

    


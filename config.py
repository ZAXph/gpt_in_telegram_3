from telebot import *

assistant_content = "Давай разберем по шагам: "
TOKEN = "6815594086:AAFmwexlJBjfNt8xinJKVhUz2613ND2opX0"

modes = ["Фантастика", "Комедия", "Страшилка"]
heroes = {"Винни-Пух", "Гермиона", "Доктор Хаус", "Наруто"}
city = {"Москва", "Хогвардс", "Рыцарское поле битвы"}
MAX_PROJECT_TOKENS = 15000  # макс. количество токенов на весь проект
MAX_USERS = 5  # макс. количество пользователей на весь проект
MAX_SESSIONS = 3  # макс. количество сессий у пользователя
MAX_TOKENS_IN_SESSION = 1000  # макс. количество токенов за сессию пользователя
token, folder_id = "t1.9euelZqXnMiZmc6bip3PjsaWmZqKye3rnpWamMyalJebnZOKxsyVypOajJTl8_d0NGZP-e98Uhlk_t3z9zRjY0_573xSGWT-zef1656Vms3Ly4uUyJfPmsqJmIqdyZCW7_zF656Vms3Ly4uUyJfPmsqJmIqdyZCWveuelZrNk5aUk5yMicfHi8eJnZPOirXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.D1aDPEiOvsXzXdvnr4KnJFbjQ0bSbEYNJr1xj8o_ri4B1ywqgAWsR28oHywzaC2i33b5DZ2USBw4Im7L_VuDBg", "b1gn1kghpq4rvsp4e2h1"
SYSTEM_PROMPT = (
    "Ты пишешь историю вместе с человеком. "
    "Историю вы пишете по очереди. Начинает человек, а ты продолжаешь. "
    "Если это уместно, ты можешь добавлять в историю диалог между персонажами. "
    "Диалоги пиши с новой строки и отделяй тире. "
    "Не пиши никакого пояснительного текста в начале, а просто логично продолжай историю."
)


def markup_create(parameter):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in parameter:
        markup.add(types.KeyboardButton(i))
    return markup


DB_NAME = 'db.sqlite'
MAX_MODEL_TOKEN = 200
HEADERS = {"Content-Type": "application/json"}
GPT_LOCAL_URL = 'http://localhost:1234/v1/chat/completions'

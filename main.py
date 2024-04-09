from repository import DATABASE
from gpt import GPT
from other import *

table = DATABASE()
gpt = GPT()
bot = TeleBot(TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)

user_data = {
    # id пользователя
    '10439284': {
        'genre': "фэнтези",  # жанр
        'character': "храбрый рыцарь",  # герой
        'setting': "пещера с драконом",  # сеттинг
        'additional_info': "в поисках потерянного артефакта."  # доп. информация
    },
    # id пользователя
    '4920572': {
        'genre': "научная фантастика",  # жанр
        'character': "космический пират",  # герой
        'setting': "орбитальная станция",  # сеттинг
        'additional_info': "на миссии по спасению родной планеты."  # доп. информация
    },
}

table.create_table()


@bot.message_handler(commands=['start'])
def send_logs(message):
    logging.info("Вывод команд")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/alltokens"))
    markup.add(types.KeyboardButton("/new_story"))
    markup.add(types.KeyboardButton("/debug"))
    bot.send_message(chat_id=message.chat.id, text="...", reply_markup=markup)


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=["alltokens"])
def mode_gpt(message):
    result = table.get_data("user_id", message.from_user.id)
    if (message.from_user.id,) not in result:
        bot.send_message(chat_id=message.chat.id,
                         text="Вы еще не создавали сценарии")
    else:
        session_id = table.get_user_session_id(message.from_user.id)
        tokens_of_session = table.get_session_size(message.from_user.id, session_id)
        if MAX_TOKENS_IN_SESSION - tokens_of_session > 0:
            bot.send_message(chat_id=message.chat.id,
                             text=f"У вас осталось: {MAX_TOKENS_IN_SESSION - tokens_of_session} токенов и {3 - session_id} сессий")
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f"У вас осталось: 0 токенов и {3 - session_id} сессий")


@bot.message_handler(commands=["new_story"])
def mode_gpt(message):
    if table.limit_user() > 5:
        bot.send_message(chat_id=message.chat.id, text="Вы не попали в список избранных")
    else:
        result = table.get_data("user_id", message.from_user.id)
        if (message.from_user.id,) not in result:
            table.add_data(message.from_user.id, 1)
            table.update_data(message.from_user.id, "token", 0)
            logging.info("Пользователь добавлен в базу данных")
        session_id = table.get_user_session_id(message.from_user.id)
        tokens = table.get_session_size(message.from_user.id, session_id)
        if tokens >= MAX_TOKENS_IN_SESSION:
            table.update_data(message.from_user.id, "session_id", session_id + 1)
            table.update_data(message.from_user.id, "token", 0)
        if table.get_user_session_id(message.from_user.id) > 3:
            bot.send_message(chat_id=message.chat.id, text="Ваше кол-во сессий закончилось")
        else:
            markup = markup_create(modes)
            msg = bot.send_message(chat_id=message.chat.id, text="Выберите Жанр", reply_markup=markup)
            bot.register_next_step_handler(msg, genre_user)


def genre_user(message):
    if message.text not in modes:
        bot.send_message(chat_id=message.chat.id, text="Вы не нажали на кнопку. Попробуйте снова!")
        bot.register_next_step_handler(message, mode_gpt)
    user_data[message.from_user.id] = {"genre": message.text}
    user_data[message.from_user.id]["additional_info"] = message.text
    markup = markup_create(heroes)
    msg = bot.send_message(chat_id=message.chat.id, text="Выберите главного героя", reply_markup=markup)
    bot.register_next_step_handler(msg, hero_user)


def genre_user_errors(message):
    msg = bot.send_message(chat_id=message.chat.id, text="Выберите главного героя")
    bot.register_next_step_handler(msg, hero_user)


def hero_user(message):
    if message.text not in heroes:
        bot.send_message(chat_id=message.chat.id, text="Вы не нажали на кнопку. Попробуйте снова!")
        bot.register_next_step_handler(message, genre_user_errors)
    user_data[message.from_user.id]['character'] = message.text
    markup = markup_create(city)
    msg = bot.send_message(chat_id=message.chat.id, text="Выберите место происходящего", reply_markup=markup)
    bot.register_next_step_handler(msg, city_user)


def hero_user_errors(message):
    msg = bot.send_message(chat_id=message.chat.id, text="Выберите место происходящего")
    bot.register_next_step_handler(msg, city_user)


def city_user(message):
    if message.text not in city:
        bot.send_message(chat_id=message.chat.id, text="Вы не нажали на кнопку. Попробуйте снова!")
        bot.register_next_step_handler(message, hero_user_errors)
    user_data[message.from_user.id]["setting"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Начать"))
    msg = bot.send_message(chat_id=message.chat.id,
                           text="Впишите дополнительную информацию, если она нужна. Если нет, то нажмите 'Начать'",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, history_create)


def history_create(message):
    if message.text != "Начать":
        user_data[message.from_user.id]['additional_info'] = message.text
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Учтем! Впишите дополнительную информацию, если она нужна. Если нет, то нажмите 'Начать'")
        bot.register_next_step_handler(msg, history_create)
    system_promt = create_prompt(user_data, message.from_user.id)
    resp = gpt.ask_gpt("...", system_promt, MAX_MODEL_TOKEN)
    bot.send_message(chat_id=message.chat.id, text=resp)
    table.update_data(message.from_user.id, "answer",
                      resp)
    session_id = table.get_user_session_id(message.from_user.id)
    tokens = table.get_session_size(message.from_user.id, session_id)
    table.update_data(message.from_user.id, "token", (tokens + len(resp) + len(system_promt)) // 2)
    is_tokens_limit(message.from_user.id, message.chat.id, bot, table)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Продолжить"))
    markup.add(types.KeyboardButton("Конец"))
    msg = bot.send_message(chat_id=message.chat.id, text="Нажми 'Продолжить' или 'Конец'", reply_markup=markup)
    bot.register_next_step_handler(msg, end_history_create)


def end_history_create(message):
    if message.text == "Продолжить":
        msg = bot.send_message(chat_id=message.chat.id, text="Продолжи составление сценария")
        bot.register_next_step_handler(msg, next_history_create)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/alltokens"))
        markup.add(types.KeyboardButton("/new_story"))
        markup.add(types.KeyboardButton("/debug"))
        result = table.get_data("answer", message.from_user.id)
        bot.send_message(chat_id=message.chat.id,
                         text=f"Вот полная история, которая у нас получилась: \n{result[0][0]}", reply_markup=markup)


def next_history_create(message):
    user_data[message.from_user.id]['additional_info'] = table.get_data("answer", message.from_user.id)
    system_promt = create_prompt(user_data, message.from_user.id)
    session_id = table.get_user_session_id(message.from_user.id)
    tokens = table.get_session_size(message.from_user.id, session_id)
    if tokens >= MAX_TOKENS_IN_SESSION:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Сценарий"))
        table.update_data(message.from_user.id, "session_id", session_id + 1)
        table.update_data(message.from_user.id, "token", 0)
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы достигли лимита токенов. Прошу, нажмите 'Сценарий' для получение полного сценария",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, end_history_create)
    else:
        if 0 < MAX_TOKENS_IN_SESSION - tokens < MAX_MODEL_TOKEN:
            resp = gpt.ask_gpt(message.text, system_promt, MAX_TOKENS_IN_SESSION - tokens)
        else:
            resp = gpt.ask_gpt(message.text, system_promt, MAX_MODEL_TOKEN)

        result = table.get_data("answer", message.from_user.id)
        tokens = table.get_session_size(message.from_user.id, session_id)
        table.update_data(message.from_user.id, "answer", result[0][0] + " " + resp)
        table.update_data(message.from_user.id, "token",
                          (tokens + len(resp) + len(system_promt) + len(message.text) // 2))
        bot.send_message(chat_id=message.chat.id, text=resp)
        is_tokens_limit(message.from_user.id, message.chat.id, bot, table)
        msg = bot.send_message(chat_id=message.chat.id, text="Продолжи составление сценария или нажми 'Конец'")
        bot.register_next_step_handler(msg, end_history_create)


bot.polling()

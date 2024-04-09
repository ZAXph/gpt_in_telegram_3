from config import *


def create_prompt(user_data, user_id):
    # Начальный текст для нашей истории - вводная часть
    prompt = SYSTEM_PROMPT

    # Добавляем в начало истории инфу о жанре и главном герое, которых выбрал пользователь
    prompt += (f"\nНапиши начало истории в стиле {user_data[user_id]['genre']} "
              f"с главным героем {user_data[user_id]['character']}. "
              f"Вот начальный сеттинг: \n{user_data[user_id]['setting']}. \n"
              "Начало должно быть коротким, 1-3 предложения.\n")

    # Если пользователь указал что-то еще в "дополнительной информации", добавляем это тоже
    if user_data[user_id]['additional_info']:
        prompt += (f"Также пользователь попросил учесть "
                   f"следующую дополнительную информацию: {user_data[user_id]['additional_info']} ")

    # Добавляем к prompt напоминание не давать пользователю лишних подсказок
    prompt += 'Не пиши никакие подсказки пользователю, что делать дальше. Он сам знает'

    # Возвращаем сформированный текст истории
    return prompt


# Функция получает идентификатор пользователя, чата и самого бота, чтобы иметь возможность отправлять сообщения
def is_tokens_limit(user_id, chat_id, bot, table):

        # Берём из таблицы идентификатор сессии
    session_id = table.get_user_session_id(user_id)
    # Получаем из таблицы размер текущей сессии в токенах
    tokens_of_session = table.get_session_size(user_id, session_id)

    # В зависимости от полученного числа выводим сообщение
    if tokens_of_session >= MAX_TOKENS_IN_SESSION:
        bot.send_message(
            chat_id,
            f'Вы израсходовали все токены в этой сессии. Вы можете начать новую, введя help_with')

    elif tokens_of_session + 50 >= MAX_TOKENS_IN_SESSION:  # Если осталось меньше 50 токенов
        bot.send_message(
            chat_id,
            f'Вы приближаетесь к лимиту в {MAX_TOKENS_IN_SESSION} токенов в этой сессии. '
            f'Ваш запрос содержит суммарно {tokens_of_session} токенов.')

    elif tokens_of_session / 2 >= MAX_TOKENS_IN_SESSION:  # Если осталось меньше половины
        bot.send_message(
            chat_id,
            f'Вы использовали больше половины токенов в этой сессии. '
            f'Ваш запрос содержит суммарно {tokens_of_session} токенов.'
        )

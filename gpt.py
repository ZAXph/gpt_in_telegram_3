import requests
from config import *


class GPT:
    def ask_gpt(self, text, system_promt, MAX_MODEL_TOKEN):
        """Запрос к Yandex GPT"""

        # Получаем токен и folder_id, так как время жизни токена 12 часов
        token, folder_id = "t1.9euelZqXnMiZmc6bip3PjsaWmZqKye3rnpWamMyalJebnZOKxsyVypOajJTl8_d0NGZP-e98Uhlk_t3z9zRjY0_573xSGWT-zef1656Vms3Ly4uUyJfPmsqJmIqdyZCW7_zF656Vms3Ly4uUyJfPmsqJmIqdyZCWveuelZrNk5aUk5yMicfHi8eJnZPOirXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.D1aDPEiOvsXzXdvnr4KnJFbjQ0bSbEYNJr1xj8o_ri4B1ywqgAWsR28oHywzaC2i33b5DZ2USBw4Im7L_VuDBg", "b1gn1kghpq4rvsp4e2h1"

        url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {
            "modelUri": f"gpt://{folder_id}/yandexgpt-lite",  # модель для генерации текста
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": MAX_MODEL_TOKEN
            },
            "messages": [
                {
                    "role": "system",  # пользователь спрашивает у модели
                    "text": system_promt  # передаём текст, на который модель будет отвечать
                },
                {
                    "role": "user",  # пользователь спрашивает у модели
                    "text": text  # передаём текст, на который модель будет отвечать
                }
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                logging.debug(f"Response {response.json()} Status code:{response.status_code} Message {response.text}")
                result = f"Status code {response.status_code}. Подробности см. в журнале."
                return result
            result = response.json()['result']['alternatives'][0]['message']['text']
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            result = "Произошла непредвиденная ошибка. Подробности см. в журнале."

        return result


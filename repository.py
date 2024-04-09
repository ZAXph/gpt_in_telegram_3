import sqlite3
from config import DB_NAME


class DATABASE:
    def __init__(self):
        self.NAME = DB_NAME

    def execute_query(self, query, data=None):
        """
        Функция для выполнения запроса к базе данных.
        Принимает имя файла базы данных, SQL-запрос и опциональные данные для вставки.
        """
        try:
            connection = sqlite3.connect(self.NAME)
            cursor = connection.cursor()

            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            cursor = cursor.fetchall()
            connection.commit()
            connection.close()
            return cursor

        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)

        finally:
            connection.close()

    def create_table(self):

        sql_query = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            session_id INTEGER,
            token INTEGER,
            answer TEXT
        );"""
        self.execute_query(sql_query)

    def add_data(self, user_id, session_id):

        sql_query = 'INSERT INTO users (user_id, session_id) VALUES (?, ?);'
        data = (user_id, session_id,)

        self.execute_query(sql_query, data)

    def update_data(self, user_id, column, value):

        sql_query = f'UPDATE users SET {column} = ? WHERE user_id = ?;'
        data = (value, user_id,)
        self.execute_query(sql_query, data)

    def get_data(self, column, user_id):
        sql_query = f'SELECT {column} FROM users WHERE user_id = ?;'
        data = (user_id,)
        result = self.execute_query(sql_query, data)
        return result

    def get_user_session_id(self, user_id):
        sql_query = f'SELECT session_id from users WHERE user_id = ?;'
        last_session_id = self.execute_query(sql_query, [user_id])[0][0]
        return last_session_id

    def get_session_size(self, user_id, session_id):
        sql_query = f'SELECT token from users WHERE user_id = ? AND session_id = ?;'
        session_size = self.execute_query(sql_query, [user_id, session_id])[0][0]
        return session_size

    def limit_user(self):
        sql_query = "SELECT count(user_id) FROM users"
        result = self.execute_query(sql_query, [])[0][0]
        print(result)
        return result

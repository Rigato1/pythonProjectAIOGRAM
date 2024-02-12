# Создаем шаблон заполнения словаря с пользователями
import sqlite3 as sq
import re
user_dict_template = {
    'bookmarks': set(),
    'index':0,
    'active_course':"Арабский язык",
    'book_name':'Мединский_курс_том_1',
    'nomer_uroka':0,
    'start':'',
    'message_id':[],
    'bot_messages':[],
    'sahihs':0,
    'Мединский_курс_том_1':'',
    'Мединский_курс_том_2':'',
    'Мединский_курс_том_3':''
}


kursi={
    "Арабский язык": {
        'Мединский_курс_том_1':{
        1:'A',
        2:'B',
        3:'C',
        4:'D',
        5:'E',
        6:'F',
        7:'G',
        8:'H',
        9:'I',
        10:'J',
        12:'K',
        13:'L',
        14:'M',
        15:'N',
        16:'O',
        17:'P',
        18:'Q',
        20:'R',
        21:'S',
        22:'T',
        23:'U'

    }}
}

# Инициализируем "базу данных"
users_db = {}

def create_new_row_for_new_user(user_id, first_name, last_name):

    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        create_query = """
            INSERT INTO users (user_id, first_name, last_name) SELECT ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE user_id = ?)
        """
        cur.execute(create_query, (user_id, first_name, last_name, user_id))
        con.commit()




#проверка на то, есть ли такой пользователь в таблице
def check_users():
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT user_id FROM users
        """)
        users = cur.fetchall()
        return users

#если такой пользователь есть в таблице, выводим его танные во временную память
def vivod_dannih(user_id):
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE user_id=?", (user_id,))
        user_data = cur.fetchall()
        result = [list(row) for row in user_data]
        return result

#сохраняем пройденные уроки в таблицу
def add_completed_topic(user_id, direction, topic):
    cleaned_value = re.sub(r'[^\w\s]', '', topic)

    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT {direction} FROM users WHERE user_id=?", (user_id,))
        current_topics = cur.fetchone()[0]  # Получаем текущее значение ячейки

        if current_topics:
            # Если значение уже есть, считаем данные из таблицы и добавляем новые данные
            new_topics = current_topics + ' ' + cleaned_value
            cur.execute(f"UPDATE users SET {direction}=? WHERE user_id=?", (new_topics, user_id))
        else:
            # Если значения нет, просто добавляем новые данные из словаря
            cur.execute(f"UPDATE users SET {direction}=? WHERE user_id=?", (cleaned_value, user_id))

        con.commit()

def sbros_galochek(user_id, direction):
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT {direction} FROM users WHERE user_id=?", (user_id,))
        current_topics = cur.fetchone()[0]  # Получаем текущее значение ячейки
        new_topics = ''
        cur.execute(f"UPDATE users SET {direction}=? WHERE user_id=?", (new_topics, user_id))








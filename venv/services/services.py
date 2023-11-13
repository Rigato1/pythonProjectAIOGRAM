#Модуль с бизнес-логикой.
from database.database import users_db
import sqlite3 as sq
from lexicon.lexicon import LEXICON


#выводит вопросы из таблицы
def get_ecsamen(table_name, start, index) -> str:
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        query = f"SELECT * FROM {table_name} WHERE idn LIKE '{start}%'"
        cur.execute(query)
        rows = cur.fetchall()
        if index < len(rows):
            return rows[index]
        else:
            return None

def kolichestvo_voprosov(table_name, start) -> str:
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        query = f"SELECT idn FROM {table_name} WHERE idn LIKE '{start}%'"
        cur.execute(query)
        rows = cur.fetchall()
        return len(rows)

def zagruzka_dannih(id, datas):
    users_db[id]['medinskiy_1_tom'] = datas[4]
    users_db[id]['medinskiy_2_tom'] = datas[5]
    users_db[id]['medinskiy_3_tom'] = datas[6]
    print(users_db[id])


#Модуль с бизнес-логикой.
from database.database import users_db
import sqlite3 as sq
from lexicon.lexicon import LEXICON

#адрес для работы в пайчарме /database/learning.db
#адрес для работы на сервере "/home/mike/pythonProjectAIOGRAM/venv/database/learning.db"

#выводит вопросы из таблицы
def get_ecsamen(table_name, start, index) -> str:
    with sq.connect("/home/mike/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        query = f"SELECT * FROM {table_name} WHERE idn LIKE '{start}%'"
        cur.execute(query)
        rows = cur.fetchall()
        if index < len(rows):
            return rows[index]
        else:
            return None

#данный код нужен чтобы вычислить сколько вопросов есть в уроке
def kolichestvo_voprosov(table_name, start) -> str:
    with sq.connect("/home/mike/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        query = f"SELECT idn FROM {table_name} WHERE idn LIKE '{start}%'"
        cur.execute(query)
        rows = cur.fetchall()
        return len(rows)

#в случае если перезагрузился сервер надо вернуть то что прошли пользователи
def zagruzka_dannih(id, datas):
    result = [list(row) for row in datas]
    for i in result:
        t1 = i[4]
        t2 = i[5]
        t3 = i[6]
        if t1 != None:
            lst = t1.replace(',', '').split()
            for x in lst:
                users_db[id]['Мединский_курс_том_1']+=x
        if t2 != None:
            lst = t2.replace(',', '').split()
            for x in lst:
                users_db[id]['Мединский_курс_том_2']+=x
        if t3 != None:
            lst = t3.replace(',', '').split()
            for x in lst:
                users_db[id]['Мединский_курс_том_3']+=x




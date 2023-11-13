import sqlite3 as sq


user_dict_template = {
    'bookmarks': set(),
    'index':2,
    'active_course':"Арабский язык",
    'book_name':'Мединский_курс_том_1',
    'nomer_uroka':1,
    'start':'C'
}

with sq.connect("learning.db") as con:
    cur = con.cursor()
    cur.execute("""
    """)
def get_ecsamen_0() -> str:
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM medinskiy
        """)
        rows = cur.fetchall()
        print(rows)

def get_ecsamen(table_name, nomer_start, index) -> str:
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        query = f"SELECT * FROM {table_name} WHERE idn LIKE '{nomer_start}%'"
        cur.execute(query)
        rows = cur.fetchall()
        print(rows[index])
        if index < len(rows):
            return rows[index]
        else:
            return None


kursi={
    'medinskiy_1_tom':{
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
    },
    'medinskiy_2_tom':{
        1:'A',
        2:'B',
        3:'C'
    }
}
def get_urok(nomer):
    a=(kursi['medinskiy_1_tom'][nomer])


get_ecsamen_0(user_dict_template['book_name'],user_dict_template['start'],user_dict_template['index'])
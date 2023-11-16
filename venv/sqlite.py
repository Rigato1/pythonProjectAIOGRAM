import sqlite3 as sq


user_dict_template = {
    'bookmarks': set(),
    'index':0,
    'active_course':"Арабский язык",
    'book_name':'Мединский_курс_том_1',
    'nomer_uroka':0,
    'start':'A',
    'message_id':[],
    'bot_messages':[],
    'sahihs':0,
    'Мединский_курс_том_1':[],
    'Мединский_курс_том_2':[],
    'Мединский_курс_том_3':[]
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
def get_danniye(id, data):
    a=(kursi['medinskiy_1_tom'][nomer])

'''def vivod_dannih(user_id, book_name):
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT {book_name} FROM users WHERE user_id=?", (user_id,))
        user_data = cur.fetchall()
        return list(user_data)

datas = vivod_dannih(1292530554, 'Мединский_курс_том_1')
for i in datas:
    print(i)'''

def vivod_dannih(user_id):
    with sq.connect("C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/database/learning.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE user_id=?", (user_id,))
        user_data = cur.fetchall()
        result = [list(row) for row in user_data]
        return result

a=1292530554
b=488834229
datas = vivod_dannih(488834229)
#result=datas.replace(',', '').split()
#print(result)

def zagruzka_dannih(id, datas):
    result = [list(row) for row in datas]
    for i in result:
        t1 = i[4]
        t2 = i[5]
        t3 = i[6]
        if t1 != None:
            lst = t1.replace(',', '').split()
            user_dict_template['Мединский_курс_том_1']=lst
        if t2 != None:
            lst = t2.replace(',', '').split()
            user_dict_template['Мединский_курс_том_2']=lst
        if t3 != None:
            user_dict_template['Мединский_курс_том_3']=lst
            lst = t3.replace(',', '').split()


zagruzka_dannih(user_dict_template['Мединский_курс_том_1'], datas)
dat=user_dict_template['Мединский_курс_том_1']
print(dat)

if 'A' in user_dict_template['Мединский_курс_том_1']:
    print(user_dict_template['Мединский_курс_том_1'])
else:
    print('A')
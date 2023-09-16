import sqlite3
import logging
import os
from aiogram import types
from config_reader import config
from datetime import datetime

class Db:

    def __init__(self):
        try:
            path = os.getcwd()+'/'+os.path.join("db", "helper.db")
            detect_types = sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            self.conn = sqlite3.connect(path, detect_types=detect_types)
        except Exception as e:
            raise sqlite3.OperationalError(e)
        self.cursor = self.conn.cursor()
        self.check_db_exists()


    def create_users(self):
        for user in config.users:
            self.insert('usr', user)


    def get_username_and_UID(self, username='', uid=0):
        s = 'select userid, username from usr where'
        s1 = s2 =  ''
        if uid:
            s1 = f"userid='{uid}'"
        if username:
            s2 = f"username='{username}'"
        if (not uid) and (not username):
            return {}
        wherelist = []
        if s1:
            wherelist.append(s1)
        if s2:
            wherelist.append(s2)
        req = ' '.join([s, ' or '.join(wherelist)])
        print(req)
        self.cursor.execute(req)
        response =  self.cursor.fetchone()
        return {'uid': response[0], 'username': response[1]}


    def update_user(self, user: types.User):
        info = {
            'userid': user.id,
            'first_name' : user.first_name,
            'last_name': user.last_name,
            'is_bot': user.is_bot,
            'username': user.username
        }
        memory = self.get_username_and_UID(username=user.username, uid=user.id)
        if memory['uid'] and (memory['uid'] == user.id):
            db.update('usr', info, {'userid': user.id})
        elif not memory['uid'] and memory['username'] == user.username:
            db.update('usr', info, {'username': user.username})
            db.insert('spend_sum', {'userid': user.id, 'amount': 0})
            db.insert('earn_sum', {'userid': user.id, 'amount': 0})
        else:
            return 0
        return 1


    def register(self, data: dict):
        _type = ''
        if data['_type']:
            _type = 'spend_sum'
        else:
            _type = 'earn_sum'
        s = f"select amount from {_type} where userid={data['usr_id']}"
        print(s)
        self.cursor.execute(s);
        total = self.cursor.fetchone()[0]
        data['created_dt'] = datetime.now().timestamp()
        db.insert("expences", data)
        db.update(_type, {'amount': total+abs(data['amount'])}, {'userid': data['usr_id']})


    def check_db_exists(self):
        check_db_exist = "SELECT name FROM sqlite_master WHERE type='table' AND name='usr'"
        self.cursor.execute(check_db_exist)
        table_exists = self.cursor.fetchall()
        if table_exists:
            return
        with open("createdb.sql", "r") as f:
            #Creating new tables if DB is empty
            sql = f.read()
            self.cursor.executescript(sql)
            self.conn.commit()
        self.create_users()


    def insert(self, table: str, column_values: dict):
        columns = ', '.join(column_values.keys())
        values = tuple(column_values.values())
        placeholders =','.join('?'*len(column_values.keys()))
        s = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(s, values)
        self.conn.commit()
        return self.cursor.lastrowid


    def where_chain(self, where_dict, operator='and'):
        where = []
        for el in where_dict.keys():
            if type(where_dict[el]) != str:
                where.append(f'{el}={where_dict[el]}')
            else:
                where.append(f"{el}='{where_dict[el]}'")
        operator = f' {operator} '
        return operator.join(where)


    def update(self, table: str, column_values: dict, filtr: dict = {}):
        cols = []
        for key in column_values.keys():
            if type(column_values[key]) != str:
                cols.append(f'{key}={column_values[key]}')
            else:
                cols.append(f"{key}='{column_values[key]}'")
        columns = ', '.join(cols)
        cols = []
        if filtr:
            where = self.where_chain(filtr, 'and')
        values = tuple(column_values.values())
        s = f'update {table} set {columns} where {where}'
        print(s)
        self.cursor.execute(s)
        self.conn.commit()




db = Db()

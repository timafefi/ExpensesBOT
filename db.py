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
    
    def init_total(self):
        self.insert('total', {'spent': 0, 'earned': 0})


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
        else:
            return 0
        return 1

    def get_total(self, earned=0, spent=0):
        s = 'select * from total'
        self.cursor.execute(s)
        answer = self.cursor.fetchall()
        ret = {}
        if answer and answer[0]:
            ret['earned'] = answer[0][0] + earned
            ret['spent'] = answer[0][1] + spent
        return ret

    def register(self, data: dict):
        data['created_dt'] = datetime.now().timestamp()
        db.insert("expences", data)
        total = {}
        if data['_type'] == 0:
            total = self.get_total(earned=data['amount'])
        else:
            total = self.get_total(spent=data['amount'])
        self.update('total', total,)


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
        self.init_total()


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
        s = ''
        for key in column_values.keys():
            if type(column_values[key]) != str and column_values[key] != None:
                cols.append(f'{key}={column_values[key]}')
            else:
                cols.append(f"{key}='{column_values[key]}'")
        columns = ', '.join(cols)
        cols = []
        if filtr:
            where = self.where_chain(filtr, 'and')
            s = f'update {table} set {columns} where {where}'
        else:
            s = f'update {table} set {columns}'
        self.cursor.execute(s)
        self.conn.commit()


    def renew_counter(self):
        for i in ['spend_sum', 'earn_sum']:
            s = f'update {i} set amount=0'
            self.cursor.execute(s)
        self.conn.commit()


    def get_users(self):
        s = 'select userid from usr'
        self.cursor.execute(s)
        return self.cursor.fetchall()


    def get_where(self, userid, date):
        l = []
        if userid:
            l.append(f'userid={userid}')
        if date:
            l.append(f"created_dt>{date}")
        return 'and'.join(l)


    def get_expences(self, userid='', date='', offset=0, limit=0):
        s = f'select usr.username, _type, category, amount, msg, created_dt '\
            f'from expences join usr on usr.userid=expences.userid'
        #where = self.get_where(userid, date)
        #query = f'{s} where {where} order by created_dt desc '\
        query = f'{s} order by created_dt desc '\
                f'limit {limit} offset {offset}'
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_sum(self, userid='', date=''):
        s = f'select _type, sum(amount) from expences'
        where = self.get_where(userid, date)
        self.cursor.execute(f'{s} where {where} group by _type')
        vals = self.cursor.fetchall()
        ans = [0, 0]
        if vals:
            ans[vals[0][0]] = vals[0][1]
            if len(vals)>1:
                ans[vals[1][0]] = vals[1][1]
        return ans
        

    def get_info(self, userid='', offset=0, limit=0, from_date=''):
        '''
        data = {
            'total': int,
            'spent':float,
            'earned':float,
            'body': ((username, _type, category, amount, msg, created_dt), ...)
        }
        '''
        data = {}
        data['body'] = self.get_expences(userid, from_date, offset, limit)
        sums = self.get_sum(userid, from_date)
        data['earned'], data['spent'] = self.get_sum(userid, from_date)
        total = self.get_total()
        data['total'] = total['earned']-total['spent']
        return data

    def count_all_expences(self):
        s = "select sum(1) from expences"
        self.cursor.execute(s)
        ans = self.cursor.fetchone()
        if ans:
            return ans[0]
        return 0


db = Db()

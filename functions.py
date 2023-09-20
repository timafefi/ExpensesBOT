from db import db
import enum
from datetime import datetime, date
from config_reader import config
from text import Emoji

OpState = enum.Enum(
    value='state',
    names=('spending', 'earning', 'zero', 'invalid')
)



def collect_and_register(data: dict):
    d = {
            'usr_id': data['id'],
            '_type': data['operation_type'],
            'amount': data['amount'],
            'category': data['category']
            }
    if d['_type'] == 1:
        d['category'] = data['category']
    print(d)
    db.register(d)


def get_operation(s):
    try:
        if s[0] == '+' or s[0] == '-':
            if float(s[0]+s[1]) > 0:
                return OpState.earning
            if float(s[0]+s[1]) < 0:
                return OpState.spending
            if float(s[0]+s[1]) == 0:
                return OpState.zero
            else:
                return OpState.invalid
        if float(s[0]) > 0:
            return OpState.earning
        if float(s[0]) < 0:
            return OpState.spending
        if float(s[0]) == 0:
            return OpState.zero
    except ValueError:
        pass
    return OpState.invalid


def cm_stamp():
    return datetime.combine(date.today().replace(day=1),
                            datetime.min.time()).timestamp()


def print_stats(data):
    s = f"{Emoji.money_bag} Баланс: {data['earned']-data['spent']}\n"\
    f"{Emoji.earn} Заработано: {data['earned']}\n"\
    f"{Emoji.spend} Потрачено: {data['spent']}\n"\
    f"_________________________________________________________________\n"\
    f"Последние операции:\n"

    tab = '   |__   '
    
    for op in data['body']:
        if op[1]:
            sign = Emoji.minus
            ts = '-'
        else:
            sign = Emoji.flyin_money
            ts = '+'
        categ = ''
        if op[2] != -1:
            categ = f"{config.categories[op[2]]}"
        person = f'\n{tab}{Emoji.person} @{op[0]}'
        msg = f'\n{tab}{Emoji.comment} <i>{op[4]}</i>' if op[4] != 'empty' else ''
        dt = datetime.fromtimestamp(op[5]).strftime("%d/%m/%y %H:%M")
        line = f"[{sign}] {dt} {categ} -> <b>{ts}{op[3]}Р</b>{person}{msg}\n"
        s = s + line
    return s



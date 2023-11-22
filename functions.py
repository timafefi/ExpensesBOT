from db import db
import enum
from datetime import datetime, date
from config_reader import config
from text import Emoji

OpState = enum.Enum(
    value='state',
    names=('spending', 'earning', 'zero', 'invalid')
)

monthdict = {
    '1': 'Январь',
    '2': 'Февраль',
    '3': 'Март',
    '4': 'Апрель',
    '5': 'Май',
    '6': 'Июнь',
    '7': 'Июль',
    '8': 'Август',
    '9': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь'
}


def collect_and_register(data: dict):
    d = {
            'usr_id': data['id'],
            '_type': data['operation_type'],
            'amount': data['amount'],
            'category': data['category']
            }
    if d['_type'] == 1:
        d['category'] = data['category']
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
    under = "_________________________________________________________________\n"
    s = f"{Emoji.money_bag} Баланс: {data['total']}\n"\
    f"{Emoji.earn} Заработано ({monthdict[str(date.today().month)]}): {data['earned']}\n"\
    f"{Emoji.spend} Потрачено ({monthdict[str(date.today().month)]}): {data['spent']}\n{under}"\
    f"Последние операции:\n"

    tab = '   |__   '
    prev_month = date.today().month
    for op in data['body']:
        curr_month = datetime.fromtimestamp(op[5]).month
        if (prev_month != curr_month):
            s = f"{s}\n{under}{monthdict[str(curr_month)]}\n{under}\n" 
            prev_month = curr_month
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



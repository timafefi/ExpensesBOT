from db import db
import enum
import datetime

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


def curr_month_timestamp():
    return datetime.combine(datetime.date().replace(day=1),
                            datetime.min.time()).timestamp()

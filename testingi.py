from datetime import date, timedelta, datetime


def create_dict_for_keyboard(month :int):
    date_one = date(2024, month, 1)
    weekday = date_one.weekday()

    one = {f'{i}':'ㅤ' for i in range(weekday)}

    while date_one < date(2024, month+1, 1):
        if date_one.weekday() != 6:
            one[f'{date_one:%d.%m.%Y}'] = 'ㅤ'
        date_one += timedelta(days=1)

    if len(one) < 30:
        while len(one) < 30:
            one[f'{len(one)}'] = 'ㅤ'
    elif 30 < len(one) < 36:
        while len(one) < 36:
            one[f'{len(one)}'] = 'ㅤ'

    return one


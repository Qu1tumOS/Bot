import datetime

days = {
    '0': 'Вс',
    '1': 'Пн',
    '2': 'Вт',
    '3': 'Ср',
    '4': 'Чт',
    '5': 'Пт',
    '6': 'Сб'
}


def print_day(rasp_date, list_days, subgroup):
    subgroup -= 1

    day = datetime.datetime.strptime(rasp_date, "%d.%m.%Y")
    date = f"""{day.strftime('%d.%m.%Y')}"""
    week = f"""{days[day.strftime('%w')]}"""

    pars = list_days[date]
    tabs = 22

    output = [f'{date[:-5].rjust(15, " ")} {week.ljust(tabs-12, " ")}']

    descript = 'ПМ.02 ПМ.05 ОП.01 ОП.02 ОП.03 ОП.04 ОП.05 ОГСЭ.04 ОГСЭ.03 ОУД.14 ОУД.04 ОУД.10 ОУД.11 ОУД.03 ОУД.07 ОП.11 ЕН.03'


    for i in pars:
        lesson = i[subgroup][0].split(' ', 1)
        cab = i[subgroup][1]

        if (lesson[0] != '') and (lesson[0] in descript):
            para = f'''{lesson[1].ljust(tabs, " ")} {cab}'''
        else:
            para = f'''{lesson[0 ]+ ' '}{lesson[1].ljust(tabs, " ")}{cab}'''

        output.append(para)

    output = '\n'.join(output)


    return output

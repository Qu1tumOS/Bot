import datetime
from config.cfg import Settings

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
    subgroup = int(subgroup)
    subgroup -= 1

    day = datetime.datetime.strptime(rasp_date, "%d.%m.%Y")
    date = f"""{day.strftime('%d.%m.%Y')}"""
    week = f"""{days[day.strftime('%w')]}"""

    pars = list_days[date]
    tabs = 24

    output = [f'{date[:-5].rjust(15, " ")} {week.ljust(tabs-12, " ")}']

    descript = Settings.descript


    for i in pars:
        lesson = i[subgroup][0]
        cab = i[subgroup][1]

        if lesson.split('.', 1)[0] in descript:
            para = lesson.split('.', 1)[1][2:]

            if para[0] == ' ':
                para = para.replace(' ', '', 1)

            lesson = f'{para.ljust(tabs, " ")} {cab}'

        output.append(lesson)

    output = '\n'.join(output)

    if week != 'Вс':
        return output
    return 'единственный выходной 🥳'

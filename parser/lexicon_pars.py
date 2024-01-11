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

    para = list_days[date]
    tabs = 22

    pars = f'{date[:-5].rjust(15, " ")} {week.ljust(tabs-12, " ")}\n' \
           f'{para[0][subgroup][0].ljust(tabs, " ")} {para[0][subgroup][1]}\n'\
           f'{para[1][subgroup][0].ljust(tabs, " ")} {para[1][subgroup][1]}\n'\
           f'{para[2][subgroup][0].ljust(tabs, " ")} {para[2][subgroup][1]}\n'\
           f'{para[3][subgroup][0].ljust(tabs, " ")} {para[3][subgroup][1]}\n'\
           f'{para[4][subgroup][0].ljust(tabs, " ")} {para[4][subgroup][1]}\n'\
           f'{para[5][subgroup][0].ljust(tabs, " ")} {para[5][subgroup][1]}\n'

    if week != 'Вс':
        return pars
    return 'единственный выходной 🥳'
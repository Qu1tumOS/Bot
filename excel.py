import pandas as pd
import openpyxl
from parser.pars import groups_list, users

def month(month):
    if month < 12:
        return list(pd.period_range(start=f'2024-{month}-01', end=f'2024-{month+1}-01', freq='D'))[:-1]
    return list(pd.period_range(start=f'2024-{month}-01', end=f'2025-01-01', freq='D'))[:-1]

lexicon_month = {1:'Январь',
                 2:'Февраль',
                 3:'Март',
                 4:'Апрель',
                 5:'Май',
                 6:'Июнь',
                 7:'Июль',
                 8:'Август',
                 9:'Сентябрь',
                 10:'Октябрь',
                 11:'Ноябрь',
                 12:'Декабрь'}

def create_table(name):
    file_name = f'{name}.xlsx'

    month_1 = pd.DataFrame(index=groups_list)
    for day in month(1):
        month_1[day] = '-'
    month_1.to_excel(file_name, sheet_name=lexicon_month[1])

    with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
        for i in range(2,13):
            page = pd.DataFrame(index=groups_list)

            for day in month(i):
                page[day] = '-'

            page.to_excel(writer, sheet_name=lexicon_month[i])

def add_stat(day, file_name):
    workbook = openpyxl.load_workbook(f'{file_name}.xlsx')
    if day[5] == '0':
        month = int(day[6])
    else:
        month = int(day[5:7])

    sheet = workbook[lexicon_month[month]]
    for i in users().items():
        for row in range(1, sheet.max_row + 1):
            if sheet.cell(row=row, column=1).value == i[0]:
                row_number = row
                break
        if row_number is not None:
            for col in range(1, sheet.max_column+1):
                if sheet.cell(row=1, column=col).value == day:
                    column_number = col
                    break
            if column_number is not None:
                cell = sheet.cell(row=row_number, column=column_number)
                cell.value = i[1]

    workbook.save(f'{file_name}.xlsx')

create_table('2024')
add_stat('2024-02-03', '2024')
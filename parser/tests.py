import requests
import datetime
import logging
from bs4 import BeautifulSoup as bs
from DataBase.db_connect import *

today = (datetime.datetime.today() + datetime.timedelta(days=0))

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('logs.txt', encoding='utf8')
file_handler.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] #%(levelname)-8s %(name)s '
           '%(funcName)s:%(lineno)d - %(message)s'))
logger.addHandler(file_handler)


def dates_in_site() -> list:
    url = 'http://raspisanie.nnst.ru/public/www/hg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    date = soup.find('li', class_='zgr').text
    last_update = soup.find('div', class_='ref').text[13:]

    date2 = datetime.date(int(date[6:10]), int(date[3:5]), int(date[:2]))
    dt2 = datetime.datetime.combine(date2, datetime.time(0, 0))

    return dt2


def group_par() -> dict:

    descript = 'ПМ. ОП. ОГСЭ. ЕН. ОУД.'
    url = 'http://raspisanie.nnst.ru/public/www/hg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('tr')

    rasp = {}

    begin = 12

    for tr in data[begin:]:
        two_subgroup_para = []
        for td in tr:
            check_para = td.find('a', class_='z1')
            check_cab = td.find('a', class_='z2')
            para = check_para.text if check_para else ' - '
            cab = check_cab.text if check_cab else ' - '

            if para.split('.', 1)[0] in descript:
                para = para.split('.', 1)[1][2:]

                if para[0] == ' ':
                    para = para.replace(' ', '', 1)



            if td.get('rowspan') == '6':
                date = td.text
                rasp[date] = []

            elif td.get('class') == ['nul']:
                if td.get('colspan') == '2':
                    rasp[date].append([[para, cab], [para, cab]])
                else:
                    if not two_subgroup_para:
                        two_subgroup_para.append([para, cab])
                    else:
                        two_subgroup_para.append([para, cab])
                        rasp[date].append(two_subgroup_para)

            elif td.get('class') == ['ur']:
                if td.get('colspan') == '2':
                    rasp[date].append([[para, cab], [para, cab]])
                else:
                    if not two_subgroup_para:
                        two_subgroup_para.append([para, cab])
                    else:
                        two_subgroup_para.append([para, cab])
                        rasp[date].append(two_subgroup_para)

    return rasp

dict_days = dict()


def view_days():
    for i in session.query(Lesson).all():
        dict_days[i.day] = i.day[:2]
    print('use view_days')
view_days()

def lessons_on_groups_add_to_table():
    logger.info('\n\n-----add lessons----- \n')
    date = dates_in_site()
    date_str = f'{date:%d.%m.%Y}'
    today_str = f'{(datetime.datetime.today() + datetime.timedelta(days=0)):%d.%m.%Y}'

    logger.info(f'date = {dates_in_site()}')
    logger.info(f'date_str = {date:%d.%m.%Y}')
    logger.info(f'today_str = {today:%d.%m.%Y}')

    if today_str in date_str and not session.query(Lesson).filter(Lesson.day==date_str).first():
        logger.info(f'added lessons day...')
        try:
            session.add(Lesson(day=date_str, lessons=group_par()))
            session.commit()
            logger.info(f'lessons add ')

        except Exception as x:
            logger.error(f'error - [{x}]')

    elif date > today and not session.query(Lesson).filter(Lesson.day==today_str).first():
        logger.info(f'added None day...')
        try:
            session.add(Lesson(day=today_str, lessons=None))
            session.commit()
            logger.info(f'None day add')

        except Exception as x:
            logger.error(f'error - [{x}]')

    view_days()


def into_data(view_day):
    day_onof = session.query(Lesson).filter(Lesson.day==f'{view_day:%d.%m.%Y}').first()
    print(day_onof.lessons, day_onof.day)

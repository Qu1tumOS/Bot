import requests
import datetime
from bs4 import BeautifulSoup as bs
from DataBase.db_connect import *



def date(offset_days: int):
    return (datetime.datetime.today() +
            datetime.timedelta(days=offset_days)).strftime('%d.%m.%Y')


all_groups = dict()
groups_name = dict()
groups_list = list()


def url_groups_update():
    print(f'\nОбновление URL групп...\n')

    url = 'http://raspisanie.nnst.ru/public/www/cg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    groups = soup.find_all('a', class_='z0')

    for group in groups:
        all_groups[group.text] = group.get('href')
        groups_name[group.text] = group.text
        groups_list.append(group.text)


url_groups_update()


def group_par(group: str) -> dict:
    global count
    url = 'http://raspisanie.nnst.ru/public/www/' + all_groups[group]

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('tr')

    rasp = {}

    begin = 13
    end = 62

    for tr in data[begin:end]:
        two_subgroup_para = []
        for td in tr:
            check_para = td.find('a', class_='z1')
            check_cab = td.find('a', class_='z2')
            para = check_para.text if check_para else ' - '
            cab = check_cab.text if check_cab else ' - '

            if td.get('rowspan') == '6':
                rasp[date := td.text[:-4]] = []

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

    print('Запрос на сайт')
    return rasp


page = 0
listt = []

def users(info=None):
    users = session.query(User).all()
    using_groups = dict()
    groups=list()
    None_users = 0

    global page
    page = 0
    for user in users:
        listt.append(user)
        if user.group != None:
            using_groups.setdefault(user.group, 0)
            using_groups[user.group] += 1
        else:
            None_users += 1

    for i in sorted(using_groups.items(), key=lambda item: item[1]):
        groups.append(f'{i[0]} - {i[1]}')
    groups.append(f'\nКоличество пользователей - {len(users) - None_users}')

    text = '\n'.join(groups)

    if info == 'text':
        return text
    return using_groups
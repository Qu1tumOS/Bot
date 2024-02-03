from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from parser.pars import url_groups_update

from parser.pars import group_par, date, users
from parser.lexicon_pars import print_day


from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


@router.callback_query(F.data == 'admin_panel')
async def open_admin_panel(callback: CallbackQuery):
    await callback.message.edit_text(
                text='ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ',
                reply_markup=create_inline_kb(1,
                                              update_url_group='Обновить группы',
                                              week_pars='пары на послезавтра',
                                              all_users='пользователи',
                                              statistics='статистика',
                                              profile='Назад')
            )
    await callback.answer()


@router.callback_query(F.data == 'update_url_group')
async def open_admin_panel(callback: CallbackQuery):
    url_groups_update()
    await callback.answer('Succes!')

@router.callback_query(F.data == 'week_pars')
async def week_pars(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    today_next = date(2)
    request_site = group_par(user.group)
    await callback.message.edit_text(
        text=f'`{print_day(today_next, request_site, user.subgroup)}`',
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(2,
                                      menu_button='Назад',
                                      update_tomorrow='Обновить')
    )

page = 0
listt = []

@router.callback_query(F.data == 'all_users')
async def open_admin_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        text=users('text'),
        reply_markup=create_inline_kb(2,
                                      admin_panel='back',
                                      view_users='смотреть профили')
    )


    await callback.answer()


@router.callback_query(F.data == 'view_users')
async def open_admin_panel(callback: CallbackQuery):
    global page, listt

    users = session.query(User).all()

    for user in users:
        listt.append(user)


    page = 0

    user = listt[page]

    print(user.name, user.user_name, user.group, user.subgroup)

    name = str(user.name).replace('<', '').replace('>', '').replace('&', '')
    user_name = str(user.user_name).replace('<', '').replace('>', '').replace('&', '')

    await callback.message.edit_text(
        text=f'@{str(name)}\n\n'\
             f'<code>Имя      {str(user_name).rjust(15, " ")}</code>\n'\
             f'<code>Группа   {str(user.group).rjust(15, " ")}</code>\n'\
             f'<code>Подгруппа{str(user.subgroup).rjust(15, " ")}</code>\n'\
             f'{page+1}/{len(users)}',
        parse_mode='HTML',
        reply_markup=create_inline_kb(2,
                                      all_users='back',
                                      next_user='->')
    )


    await callback.answer()


@router.callback_query(F.data == 'next_user')
async def open_admin_panel(callback: CallbackQuery):
    global page, listt

    users = session.query(User).all()

    for user in users:
        listt.append(user)


    if page < len(users)-1:
        page += 1


        user = listt[page]

        print(user.name, user.user_name, user.group, user.subgroup)

        name = str(user.name).replace('<', '').replace('>', '').replace('&', '')
        user_name = str(user.user_name).replace('<', '').replace('>', '').replace('&', '')

        await callback.message.edit_text(
            text=f'@{str(name)}\n\n'\
                f'<code>Имя      {str(user_name).rjust(15, " ")}</code>\n'\
                f'<code>Группа   {str(user.group).rjust(15, " ")}</code>\n'\
                f'<code>Подгруппа{str(user.subgroup).rjust(15, " ")}</code>\n'\
                f'{page+1}/{len(users)}',
            parse_mode='HTML',
            reply_markup=create_inline_kb(2,
                                          forward_user='<-',
                                          next_user='->',
                                          all_users='back'
                                          )
        )
    else:
        await callback.message.edit_text(
            text='больше пользователей нет',
            reply_markup=create_inline_kb(2,
                                          forward_user='<-',
                                          all_users='back'
                                          )
        )

    await callback.answer()


@router.callback_query(F.data == 'forward_user')
async def open_admin_panel(callback: CallbackQuery):
    global page, listt

    users = session.query(User).all()

    for user in users:
        listt.append(user)


    if page > 0:
        page -= 1


        user = listt[page]

        print(user.name, user.user_name, user.group, user.subgroup)

        name = str(user.name).replace('<', '').replace('>', '').replace('&', '')
        user_name = str(user.user_name).replace('<', '').replace('>', '').replace('&', '')

        await callback.message.edit_text(
            text=f'@{str(name)}\n\n'\
                f'<code>Имя      {str(user_name).rjust(15, " ")}</code>\n'\
                f'<code>Группа   {str(user.group).rjust(15, " ")}</code>\n'\
                f'<code>Подгруппа{str(user.subgroup).rjust(15, " ")}</code>\n'\
                f'{page+1}/{len(users)}',
            parse_mode='HTML',
            reply_markup=create_inline_kb(2,
                                          forward_user='<-',
                                          next_user='->',
                                          all_users='back'
                                          )
        )
    else:
        page = -1
        await callback.message.edit_text(
            text='больше пользователей нет',
            reply_markup=create_inline_kb(2,
                                          all_users='back',
                                          next_user='->'
                                          )
        )

    await callback.answer()


@router.callback_query(F.data == 'statistics')
async def statistics(callback: CallbackQuery):
    dock = FSInputFile('2024.xlsx')
    await callback.message.reply_document(dock,
                                          caption='статистика по количеству пользователей',
                                          reply_markup=create_inline_kb(1,
                                                                        del_document='удалить'))
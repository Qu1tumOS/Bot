from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from parser.pars import url_groups_update

from parser.pars import group_par, date, users
from parser.lexicon_pars import print_day


from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


page = 0
listt = []

@router.callback_query(F.data == 'view_users')
async def open_admin_panel(callback: CallbackQuery):
    global page, listt

    users = session.query(User).filter(User.name != None).all()

    for user in users:
        listt.append(user)


    page = 0

    user = listt[page]


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
                                      statistics='back',
                                      next_user='->')
    )


    await callback.answer()


@router.callback_query(F.data == 'next_user')
async def open_admin_panel(callback: CallbackQuery):
    global page, listt

    users = session.query(User).filter(User.name != None).all()

    for user in users:
        listt.append(user)


    if page < len(users)-2:
        page += 1


        user = listt[page]


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
                                          statistics='back'
                                          )
        )
    else:
        page += 1


        user = listt[page]


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
                                          statistics='back'
                                          )
        )


@router.callback_query(F.data == 'forward_user')
async def open_admin_panel(callback: CallbackQuery):
    global page, listt

    users = session.query(User).filter(User.name != None).all()

    for user in users:
        listt.append(user)


    if page > 1:
        page -= 1


        user = listt[page]


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
                                          statistics='back'
                                          )
        )
    else:
        page -= 1


        user = listt[page]


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
                                          statistics='back',
                                          next_user='->')
        )
    await callback.answer()

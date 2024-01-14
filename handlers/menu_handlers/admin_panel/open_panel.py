from aiogram import Router, F
from aiogram.types import CallbackQuery

from parser.pars import url_groups_update

from parser.pars import group_par, date
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

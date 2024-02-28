from aiogram import Router, F
from aiogram.types import CallbackQuery

from parser.pars import url_groups_update

from parser.pars import group_par, date, users
from parser.lexicon_pars import print_day


from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *

router = Router()


@router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        text='ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ',
        reply_markup=create_inline_kb(1,
                                      update_url_group='Обновить группы',
                                      beta_test_panel='бета функции',
                                      statistics='статистика',
                                      profile='Назад')
            )
    await callback.answer()


@router.callback_query(F.data == 'update_url_group')
async def update_url_group(callback: CallbackQuery):
    url_groups_update()
    await callback.answer('Succes!')

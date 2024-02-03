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
                                      all_users='пользователи',
                                      statistics='статистика',
                                      profile='Назад')
            )
    await callback.answer()


@router.callback_query(F.data == 'update_url_group')
async def open_admin_panel(callback: CallbackQuery):
    url_groups_update()
    await callback.answer('Succes!')

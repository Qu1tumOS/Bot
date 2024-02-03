from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from excel import create_table, add_stat

import datetime

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


today = (datetime.datetime.today() + datetime.timedelta(days=0)).strftime('%Y-%m-%d')

@router.callback_query(F.data == 'statistics')
async def statistics(callback: CallbackQuery):
    await callback.message.edit_text(
        text='text suuuu',
        reply_markup=create_inline_kb(1,
                                      add_table='создать новую таблицу',
                                      update_stats='добавить статистику',
                                      send_stats='отправить таблицу'
        )
    )


@router.callback_query(F.data == 'add_table')
async def add_table(callback: CallbackQuery):
    await callback.message.edit_text(
        text='точно???',
        reply_markup=create_inline_kb(1,
                                      verify_add_stats='ДА',
                                      statistics='назад')
    )


@router.callback_query(F.data == 'verify_add_stats')
async def verify_add_stats(callback: CallbackQuery):
    create_table('2024')

@router.callback_query(F.data == 'update_stats')
async def update_stats(callback: CallbackQuery):
    add_stat(today, '2024')


@router.callback_query(F.data == 'send_stats')
async def send_stats(callback: CallbackQuery):
    dock = FSInputFile('2024.xlsx')
    await callback.message.reply_document(dock,
                                          caption='статистика по количеству пользователей',
                                          reply_markup=create_inline_kb(1,
                                                                        del_document='удалить'))
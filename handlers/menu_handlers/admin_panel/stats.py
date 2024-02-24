from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from excel import create_table
from parser.pars import users
from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


@router.callback_query(F.data == 'statistics')
async def statistics(callback: CallbackQuery):
    await callback.message.edit_text(
        text=users('text'),
        reply_markup=create_inline_kb(1,
                                      add_table='создать новую таблицу',
                                      view_users='смотреть профили',
                                      send_stats='отправить таблицы',
                                      admin_panel='назад'
        )
    )
    await callback.answer()


@router.callback_query(F.data == 'add_table')
async def add_table(callback: CallbackQuery):
    await callback.message.edit_text(
        text='точно???',
        reply_markup=create_inline_kb(1,
                                      verify_add_stats='ДА',
                                      statistics='назад')
    )
    await callback.answer()

@router.callback_query(F.data == 'verify_add_stats')
async def verify_add_stats(callback: CallbackQuery):
    create_table('2024')
    await callback.message.edit_text(
        text=users('text'),
        reply_markup=create_inline_kb(1,
                                      add_table='создать новую таблицу',
                                      update_stats='добавить статистику',
                                      send_stats='отправить таблицы',
                                      admin_panel='назад'
        )
    )
    await callback.answer()

@router.callback_query(F.data == 'send_stats')
async def send_stats(callback: CallbackQuery):
    dock = FSInputFile('2024.xlsx')
    logs = FSInputFile('logs.txt')
    await callback.message.reply_document(dock,
                                          caption='статистика по количеству пользователей',
                                          reply_markup=create_inline_kb(1,
                                                                        del_document='удалить'))
    await callback.message.reply_document(
        logs,
        caption='логи',
                                          reply_markup=create_inline_kb(1,
                                                                        del_document='удалить'))
    await callback.answer()

@router.callback_query(F.data == 'del_document')
async def del_document(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
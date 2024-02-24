from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
import datetime
from keyboards.keyboard_creator import create_inline_kb
from parser.pars import all_groups, groups_name
from DataBase.db_connect import *

from excel import add_stat, today
import logging


logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('logs.txt', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] #%(levelname)-8s %(name)s '
           '%(funcName)s:%(lineno)d - %(message)s'))
logger.addHandler(file_handler)


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
            text="Войди в аккаунт или пройди небольшую регистрацию",
            reply_markup=create_inline_kb(1,
                                        log_button='Вход')
            )


@router.callback_query(F.data == 'log_button')
async def log(callback: CallbackQuery):
    user_info = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    if user_info == None:
        session.add(User(tg_id=callback.from_user.id,
                         name=callback.from_user.username,
                         user_name=callback.from_user.first_name))
        session.commit()
        await callback.message.edit_text(
            text=f'''Выбери техникум:''',
            reply_markup=create_inline_kb(1,
                                          NST='НСТ')
    )

    elif user_info.group == None:
        await callback.message.edit_text(
            text='Выбери свою группу и подгруппу',
            reply_markup=create_inline_kb(6,
                                          **groups_name)
    )

    else:
        await callback.message.edit_text(
            text='ㅤㅤㅤㅤГлавное меню\nпосмотреть расписание на:',
            reply_markup=create_inline_kb(2,
                                          today_button='Сегодня',
                                          tomorrow_button='Завтра',
                                          profile='Меню')
    )
    await callback.answer()


@router.callback_query(F.data == 'NST')
async def add_collage_nst(callback: CallbackQuery):
    user_info = session.query(User).filter(User.tg_id==callback.from_user.id).first()
    user_info.collage = 'НСТ'
    session.commit()
    await callback.message.edit_text(
        text='Выбери свою группу',
        reply_markup=create_inline_kb(6,
                                      **groups_name)
    )
    await callback.answer()


@router.callback_query(F.data.in_(all_groups))
async def add_group(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
    user.group = callback.data
    session.commit()
    if user.subgroup == None:
        await callback.message.edit_text(
            text='Окей, осталось выбрать подгруппу',
            reply_markup=create_inline_kb(2,
                                          subgroup_1='1',
                                          subgroup_2='2',
                                          NST='Назад')
        )
    else:
        await callback.message.edit_text(
            text=f'@{str(user.name)}\n\n'\
             f'<code>Имя      {str(user.user_name).rjust(15, " ")}</code>\n'\
             f'<code>Техникум {str(user.collage).rjust(15, " ")}</code>\n'\
             f'<code>Группа   {str(user.group).rjust(15, " ")}</code>\n'\
             f'<code>Подгруппа{str(user.subgroup).rjust(15, " ")}</code>',
        parse_mode='HTML',
            reply_markup=create_inline_kb(2,
                                        edit_profile='Изменить',
                                        delete_profile='Удалить',
                                        profile='Назад')
        )
    await callback.answer()


@router.callback_query(F.data.in_(['subgroup_1', 'subgroup_2']))
async def add_subgroup(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    if user.subgroup == None:
        logger.info(f'НОВЫЙ ПОЛЬЗОВАТЕЛЬ {user.user_name} @{user.name}\n')
        add_stat(today, '2024')
        logger.info('СТАТИСТИКА ОБНОВЛЕНА ПОСЛЕ РЕГИСТРАЦИИ\n')

    user.subgroup = callback.data[-1]
    session.commit()
    await callback.message.edit_text(
        text='ㅤㅤㅤㅤГлавное меню\nпосмотреть расписание на:',
        reply_markup=create_inline_kb(2,
                                      today_button='Сегодня',
                                      tomorrow_button='Завтра',
                                      profile='Меню')
    )
    await callback.answer()



@router.callback_query(F.data == 'menu_button')
async def main_page(callback: CallbackQuery):
    await callback.message.edit_text(
        text='ㅤㅤㅤㅤГлавное меню\nпосмотреть расписание на:',
        reply_markup=create_inline_kb(2,
                                      today_button='Сегодня',
                                      tomorrow_button='Завтра',
                                      profile='Меню')
    )
    await callback.answer()

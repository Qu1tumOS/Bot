from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart

from keyboards.keyboard_creator import create_inline_kb
from parser.pars import all_groups, groups_name
from DataBase.db_connect import *


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    user = session.query(User).filter(User.tg_id==message.from_user.id).first()
    if user == None:
        await message.answer(
            text="Войди в аккаунт или пройди небольшую регистрацию",
            reply_markup=create_inline_kb(1,
                                        log_button='Вход')
            )
    else:
        await message.delete()


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
    await callback.message.edit_text(text='Выбери свою группу',
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
            text=f'@{user.name}\n'\
                f'\n'\
                f'`Имя      {str(user.user_name).rjust(15, " ")}`\n'\
                f'`Техникум {str(user.collage).rjust(15, " ")}`\n'\
                f'`Группа   {str(user.group).rjust(15, " ")}`\n'\
                f'`Подгруппа{str(user.subgroup).rjust(15, " ")}`',
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(2,
                                        edit_profile='Изменить',
                                        delete_profile='Удалить',
                                        profile='Назад')
        )
    await callback.answer()


@router.callback_query(F.data.in_(['subgroup_1', 'subgroup_2']))
async def add_subgroup(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
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
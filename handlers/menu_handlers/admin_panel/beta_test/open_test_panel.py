from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.keyboard_creator import create_inline_kb
from parser.tests import dict_days, view_days
import datetime

from DataBase.db_connect import *

from environs import Env

env = Env()
env.read_env()

router = Router()


@router.callback_query(F.data == 'beta_test_panel')
async def beta_test_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        text='BETA FUNCTION',
        reply_markup=create_inline_kb(1,
                                      beta_new_menu='бета главное меню',
                                      bd_settings='БД',
                                      send_invoice='отправка сообщения всем пользователям',
                                      admin_panel='назад'
                                      )
    )
    await callback.answer()

@router.callback_query(F.data == 'bd_settings')
async def bd_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'Выбери базу данных',
        reply_markup=create_inline_kb(1,
                                      Lesson='lessons_on_groups',
                                      beta_test_panel='назад'
        )
    )

@router.callback_query(F.data == 'Lesson')
async def lesson(callback: CallbackQuery):
    await callback.message.edit_text(
        text='добаваить/удалить',
        reply_markup=create_inline_kb(1,
                                      lesson_add='добавить',
                                      lesson_del='удалить',
                                      bd_settings='назад')
    )

@router.callback_query(F.data == 'lesson_del')
async def lesson_del(callback: CallbackQuery):

    data_list = {f'Lesson_del:{x.day}': x.day for x in session.query(Lesson).all()}
    await callback.message.edit_text(
        text='delete data',
        reply_markup=create_inline_kb(1,
                                      **data_list,
                                      Lesson='назад')
    )

@router.callback_query(F.data.in_([f'Lesson_del:{i.day}' for i in session.query(Lesson).all()]))
async def del_lesson_data(callback: CallbackQuery):
    day = callback.data.split(':')[1]
    session.query(Lesson).filter(Lesson.day == day).delete(synchronize_session="fetch")
    session.commit()

    view_days()
    
    data_list = {f'Lesson_del:{x.day}': x.day for x in session.query(Lesson).all()}
    await callback.message.edit_text(
        text='delete data',
        reply_markup=create_inline_kb(1,
                                      **data_list,
                                      Lesson='назад')
    )
    await callback.answer(f'delete {day}')



#пары, быстрый доступ, меню
@router.callback_query(F.data == 'beta_new_menu')
async def beta_new_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text='BETA FUNCTION <new menu>',
        reply_markup=create_inline_kb(2,
                                      beta_button='пары',
                                      beta_test_panel='меню',
                                      beta_button_2='быстрый доступ',
                                      )
    )
    await callback.answer()


@router.callback_query(F.data == 'beta_button')
async def beta_button(callback: CallbackQuery):
    await callback.answer(f'today - {(datetime.datetime.today() + datetime.timedelta(days=0)):%d.%m.%Y}')

@router.callback_query(F.data == 'beta_button_2')
async def beta_button_2(callback: CallbackQuery):
    await callback.message.edit_text(
        text='BETA FUNCTION <new menu>',
        reply_markup=create_inline_kb(len(dict_days) if len(dict_days) < 6 else 6 if len(dict_days) != 0 else 1,
                                      **dict_days,
                                      beta_new_menu='назад'))
    await callback.answer('бета')

@router.callback_query(F.data.in_(dict_days))
async def print_day(callback: CallbackQuery):
    data = session.query(Lesson).filter(Lesson.day==callback.data).first().lessons
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
    subgroup = int(user.subgroup) - 1

    tabs = 24

    if data != None:
        output = [f'{callback.data.rjust(15, " ")}']
        for i in data[user.group]:
            para = i[subgroup][0]
            cab = i[subgroup][1]

            lesson = f'{para.ljust(tabs, " ")} {cab}'

            output.append(lesson)
        output = '\n'.join(output)

        await callback.message.edit_text(
        text=f'`{output}`',
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(2,
                                      beta_button_2='назад'))
    else:
        await callback.answer('в этот день пар не было')
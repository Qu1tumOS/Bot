from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.keyboard_creator import create_inline_kb
from parser.tests import dict_days

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
                                      send_invoice='отправка сообщения всем пользователям',
                                      admin_panel='назад'
                                      )
    )
    await callback.answer()


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
    await callback.answer('бета кнопка')

@router.callback_query(F.data == 'beta_button_2')
async def beta_button_2(callback: CallbackQuery):
    await callback.message.edit_text(
        text='BETA FUNCTION <new menu>',
        reply_markup=create_inline_kb(len(dict_days) if len(dict_days) != 0 else 1 if len(dict_days) < 6 else 6,
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
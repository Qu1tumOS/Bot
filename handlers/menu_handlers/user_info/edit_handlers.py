from aiogram import Router, F
from aiogram.types import CallbackQuery

from parser.pars import groups_name
from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


@router.callback_query(F.data == 'edit_profile')
async def edit_profile(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выбери что нужно изменить',
        reply_markup=create_inline_kb(1,
                                      edit_group='Группу',
                                      edit_subgroup='Подгруппу',
                                      user_info='Назад')
    )
    await callback.answer()


@router.callback_query(F.data == 'edit_group')
async def edit_group(callback: CallbackQuery):
    await callback.message.edit_text(text='Выбери свою группу',
                                     reply_markup=create_inline_kb(6,
                                                                   **groups_name,
                                                                   edit_profile='Назад')
                                     )
    await callback.answer()


@router.callback_query(F.data == 'edit_subgroup')
async def edit_subgroup(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выбери новую подгруппу',
        reply_markup=create_inline_kb(2,
                                      edit_subgroup_1='1',
                                      edit_subgroup_2='2',
                                      edit_profile='Назад')
        )

@router.callback_query(F.data.in_(['edit_subgroup_1', 'edit_subgroup_2']))
async def add_subgroup(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
    user.subgroup = callback.data[-1]
    session.commit()
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
from aiogram import Router, F
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from parser.pars import all_groups, groups_name

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *



router = Router()

class RegisterCheck(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
        return user == None

class GroupCheck(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
        return user.group == None or user.subgroup == None


@router.callback_query(F.data != 'log_button', RegisterCheck())
async def check_register(callback: CallbackQuery):
    await callback.message.edit_text(
        text='тебя нет в базе',
        reply_markup=create_inline_kb(1,
                                      log_button='Регистрация')
    )
    await callback.answer()

@router.callback_query(~F.data.in_(all_groups), ~F.data.in_(['subgroup_1', 'subgroup_2', 'log_button', 'NST']), GroupCheck())
async def check_group(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    if user.group == None:
        await callback.message.edit_text(
            text='Для начала выбери свою группу и подгруппу',
            reply_markup=create_inline_kb(6,
                                        **groups_name)
        )

    elif user.subgroup == None:
        await callback.message.edit_text(
            text='Для начала выбери свою подгруппу',
            reply_markup=create_inline_kb(2,
                                          subgroup_1='1',
                                          subgroup_2='2',
                                          NST='Назад')
        )

    else:
         await callback.message.edit_text(
            text=f'{callback.data}',
            reply_markup=create_inline_kb(2,
                                          subgroup_1='1',
                                          subgroup_2='2',
                                          NST='Назад')
        )
    await callback.answer()

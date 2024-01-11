from aiogram import Router, F
from aiogram.types import CallbackQuery

from environs import Env

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()

env = Env()
env.read_env()


@router.callback_query(F.data == 'profile')
async def open_profile(callback: CallbackQuery):
    if str(callback.from_user.id) in env('ADMIN_ID'):
        await callback.message.edit_text(
            text='ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ',
            reply_markup=create_inline_kb(1,
                                        user_info='Профиль🎅',
                                        # user_friends='Друзья',
                                        # support='Поддержка',
                                        # admin_panel='Админ панель',
                                        menu_button='Назад')
        )
    else:
        await callback.message.edit_text(
            text='ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ',
            reply_markup=create_inline_kb(1,
                                        user_info='Профиль🎅',
                                        # user_friends='Друзья',
                                        # support='Поддержка👤',
                                        menu_button='Назад')
        )
    await callback.answer()

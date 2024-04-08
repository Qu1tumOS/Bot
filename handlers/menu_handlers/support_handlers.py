from aiogram import Router, F
from aiogram.types import CallbackQuery

from environs import Env

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()

@router.callback_query(F.data == 'support')
async def support(callback: CallbackQuery):
    await callback.message.edit_text(
                text='По всем вопросам пишите ему\n@Qu1tum',
                reply_markup=create_inline_kb(1,
                                              profile='Назад')
            )
    await callback.answer()
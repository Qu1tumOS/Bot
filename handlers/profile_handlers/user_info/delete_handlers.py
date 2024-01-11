from aiogram import Router, F
from aiogram.types import CallbackQuery

from parser.pars import group_par, date
from parser.lexicon_pars import print_day

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


@router.callback_query(F.data == 'delete_profile')
async def delete_profile(callback: CallbackQuery):
    session.query(User).filter(User.tg_id==callback.from_user.id).delete(synchronize_session="fetch")
    session.commit()
    await callback.message.edit_text(
        text='Твой профиль удален',
        reply_markup=create_inline_kb(1,
                                      log_button='Регистрация')
    )
    await callback.answer()
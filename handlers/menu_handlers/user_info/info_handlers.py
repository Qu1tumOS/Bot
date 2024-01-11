from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


@router.callback_query(F.data == 'user_info')
async def user_info(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
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

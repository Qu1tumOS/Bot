from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


@router.callback_query(F.data == 'user_info')
async def user_info(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    user.name = callback.from_user.username
    user.user_name = callback.from_user.first_name
    
    name = str(user.name).replace('<', '').replace('>', '').replace('&', '')
    user_name = str(user.user_name).replace('<', '').replace('>', '').replace('&', '')

    await callback.message.edit_text(
        text=f'@{str(name)}\n\n'\
             f'<code>Имя      {str(user_name).rjust(15, " ")}</code>\n'\
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

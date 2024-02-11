from environs import Env
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.keyboard_creator import create_inline_kb

env = Env()
env.read_env()

router = Router()



@router.callback_query(F.data == 'pay_money')
async def pay_money(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Если хотите поддержать проект, буду сильно благодарен :)',
        reply_markup=create_inline_kb(1,
                                      url_button='помочь',
                                      profile='назад'))
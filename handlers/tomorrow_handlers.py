from aiogram import Router, F
from aiogram.types import CallbackQuery

from parser.pars import group_par, date
from parser.lexicon_pars import print_day

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *


router = Router()


@router.callback_query(F.data == 'tomorrow_button')
async def tomorrow(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    tomorrow = date(1)
    next_day = date(2)
    week_pars = group_par(user.group)

    if tomorrow in week_pars:
        check = print_day(tomorrow, week_pars, user.subgroup)
        if check != 'единственный выходной 🥳':
            await callback.message.edit_text(
                text=f'`{check}`',
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(2,
                                              menu_button='Назад',
                                              update_tomorrow='Обновить')
            )
        else:
            await callback.message.edit_text(
            text=f'`{print_day(next_day, week_pars, user.subgroup)}`',
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(2,
                                          menu_button='Назад',
                                          update_tomorrow='Обновить')
            )
            await callback.answer(text='Пары на понедельник')
    else:
        await callback.message.edit_text(
            text='Завтра пар не будет',
            reply_markup=create_inline_kb(1,
                                          menu_button='Назад'))
    await callback.answer()


@router.callback_query(F.data == 'update_tomorrow')
async def update_tomorrow(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    today = date(1)
    week_pars = group_par(user.group)

    if today in week_pars:
        check = print_day(today, week_pars, user.subgroup)
        if callback.message.text not in check:
            await callback.message.edit_text(
                text=f'`{check}`',
                parse_mode='MarkdownV2',
                reply_markup=callback.message.reply_markup
            )
            await callback.answer(text='Обновлено ✅')

        else:
            await callback.answer(text='Расписание не изменилось ✅')
    else:
        await callback.message.edit_text(
            text='завтра пар не будет',
            reply_markup=create_inline_kb(2,
                                          menu_button='Назад'))
        await callback.answer(text='Обновлено ✅')

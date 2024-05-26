from aiogram import Router, F
from aiogram.types import CallbackQuery

from parser.pars import group_par, date
from parser.lexicon_pars import print_day

from keyboards.keyboard_creator import create_inline_kb

from DataBase.db_connect import *
import datetime
import logging


router = Router()

@router.callback_query(F.data == 'today_button')
async def today(callback: CallbackQuery):
    dt_today = datetime.datetime.today()
    today = f'{dt_today:%d.%m.%Y}'

    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
    data = session.query(Lesson).filter(Lesson.day==today).first()

    week_pars = group_par(user.group)

    if today in week_pars:
        print_schedule = print_day(today, week_pars, user.subgroup)
        if callback.message.text not in print_schedule:
            await callback.message.edit_text(
                text=f'`{print_schedule}`',
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(2,
                                              menu_button='Назад',
                                              update_today='Обновить')
            )

    elif data and dt_today.weekday() != 6:
        subgroup = int(user.subgroup) - 1

        tabs = 24

        if data:
            output = [f'{today[:5].rjust(19, " ")}']
            for i in data.lessons[user.group]:
                para = i[subgroup][0]
                cab = i[subgroup][1]

                lesson = f'{para.ljust(tabs, " ")} {cab}'

                output.append(lesson)
            output = '\n'.join(output)

            await callback.message.edit_text(
            text=f'`{output}`',
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(2,
                                          menu_button='Назад',
                                          tomorrow_button='Пары завтра'))
            await callback.answer()

    else:
        await callback.message.edit_text(
            text=f'Сегодня пар уже не будет',
            reply_markup=create_inline_kb(2,
                                          menu_button='Назад',
                                          tomorrow_button='Пары завтра'))
    await callback.answer()


@router.callback_query(F.data == 'update_today')
async def update_today(callback: CallbackQuery):
    dt_today = datetime.datetime.today()
    today = f'{dt_today:%d.%m.%Y}'

    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()
    data = session.query(Lesson).filter(Lesson.day==today).first()


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

    elif data and dt_today.weekday() != 6:
        subgroup = int(user.subgroup) - 1

        tabs = 24

        if data:
            output = [f'{today[:5].rjust(19, " ")}']
            for i in data.lessons[user.group]:
                para = i[subgroup][0]
                cab = i[subgroup][1]

                lesson = f'{para.ljust(tabs, " ")} {cab}'

                output.append(lesson)
            output = '\n'.join(output)

            await callback.message.edit_text(
            text=f'`{output}`',
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(2,
                                          menu_button='Назад',
                                          next_day_par='Пары завтра'))
            await callback.answer()

    else:
        await callback.message.edit_text(
            text='Сегодня пар уже не будет',
            reply_markup=create_inline_kb(2,
                                          menu_button='Назад',
                                          next_day_par='Пары завтра'))
        await callback.answer(text='Обновлено ✅')


@router.callback_query(F.data == 'next_day_par')
async def not_today(callback: CallbackQuery):
    user = session.query(User).filter(User.tg_id==callback.from_user.id).first()

    today = date(1)
    week_pars = group_par(user.group)

    if today in week_pars:
        check = print_day(today, week_pars, user.subgroup)
        await callback.message.edit_text(
            text=f'`{check}`',
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(2,
                                    menu_button='Назад',
                                    update_tomorrow='Обновить')
        )
    elif session.query(Lesson).filter(Lesson.day==callback.data).first().lessons:
        pass

    else:
        await callback.message.edit_text(
            text='завтра пар не будет',
            reply_markup=create_inline_kb(2,
                                          menu_button='Назад'))

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from parser.pars import url_groups_update
from parser.pars import group_par, date, users
from parser.lexicon_pars import print_day
from keyboards.keyboard_creator import create_inline_kb
from DataBase.db_connect import *

from environs import Env

env = Env()
env.read_env()

router = Router()

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('logs.txt', encoding='utf8')
file_handler.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] #%(levelname)-8s %(name)s '
           '%(funcName)s:%(lineno)d - %(message)s'))
logger.addHandler(file_handler)


class FSMSendMessage(StatesGroup):
    send_invoice_state = State()
    text: str
    count_use = set()
    admin_id = int(env('ADMIN_ID'))


@router.callback_query(F.data == 'send_invoice')
async def send_invoice(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f'прошлое сообщение прочитало {len(FSMSendMessage.count_use)} человек\n\nВведите новое сообщение для пользователей:',
        reply_markup=create_inline_kb(1,
                                      dont_send_invoice='Назад')
    )
    await state.set_state(FSMSendMessage.send_invoice_state)
    await callback.answer()

@router.callback_query(F.data == 'dont_send_invoice')
async def dont_send_invoice(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='BETA FUNCTION',
        reply_markup=create_inline_kb(1,
                                      beta_new_menu='бета главное меню',
                                      send_invoice='отправка сообщения всем пользователям',
                                      admin_panel='назад'
                                      )
    )
    await state.clear()
    await callback.answer()

@router.message(StateFilter(FSMSendMessage.send_invoice_state))
async def send_text_message(message: Message, state: FSMContext):
    FSMSendMessage.text = message.text
    await message.delete()
    await state.clear()
    await message.answer(text=f'отправить сообщение:\n\n{FSMSendMessage.text}',
                         reply_markup=create_inline_kb(1,
                                                       yes_invoice_message='Отправить',
                                                       test_invoice_message='тестовая отправка',
                                                       no_invoice_message='Отмена'))


@router.callback_query(F.data == 'yes_invoice_message')
async def yes_invoice_message(callback: CallbackQuery):
    try:
        await callback.message.delete()
        FSMSendMessage.count_use.clear()
        users = session.query(User).all()
        message_text = FSMSendMessage.text

        for user in users:
            await callback.bot.send_message(
                chat_id=user.tg_id,
                text=message_text,
                reply_markup=create_inline_kb(1,
                                              url_button='поддержать проект',
                                              del_invoice='удалить сообщение'))
        await callback.answer()

        logger.info(f'отправлено сообщение <{message_text}>')
    except Exception as x:
        logger.warning(f'СООБЩЕНИЕ НЕ ОТПРАВЛЕНО\n{x}')

@router.callback_query(F.data == 'test_invoice_message')
async def test_invoice_message(callback: CallbackQuery):
    try:
        await callback.message.delete()
        message_text = FSMSendMessage.text
        chat = FSMSendMessage.admin_id

        await callback.bot.send_message(
            chat_id=chat,
            text=message_text,
            reply_markup=create_inline_kb(1,
                                          url_button='поддержать проект',
                                          del_test_invoice='удалить сообщение',
                                          yes_invoice_message='Отправить всем'))
        await callback.answer()

        logger.info(f'отправлено тестовое сообщение<{message_text}>')
    except Exception as x:
        logger.warning(f'ТЕСТОВОЕ СООБЩЕНИЕ НЕ ОТПРАВЛЕНО\n{x}')

@router.callback_query(F.data == 'no_invoice_message')
async def send_invoice2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMSendMessage.send_invoice_state)
    await callback.message.delete()


@router.callback_query(F.data == 'del_invoice')
async def del_invoice(callback: CallbackQuery):
    await callback.message.delete()
    FSMSendMessage.count_use.add(callback.from_user.id)
    await callback.answer()

@router.callback_query(F.data == 'del_test_invoice')
async def del_test_invoice(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(FSMSendMessage.send_invoice_state)
    await callback.answer()

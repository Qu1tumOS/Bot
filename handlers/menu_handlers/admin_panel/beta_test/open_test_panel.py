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


@router.callback_query(F.data == 'beta_test_panel')
async def beta_test_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        text='BETA FUNCTION',
        reply_markup=create_inline_kb(1,
                                      beta_new_menu='бета главное меню',
                                      send_invoice='отправка сообщения всем пользователям',
                                      admin_panel='назад'
                                      )
    )
    await callback.answer()


#пары, быстрый доступ, меню
@router.callback_query(F.data == 'beta_new_menu')
async def beta_new_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text='BETA FUNCTION <new menu>',
        reply_markup=create_inline_kb(2,
                                      beta_button='пары',
                                      beta_test_panel='меню',
                                      beta_button_2='быстрый доступ',
                                      )
    )
    await callback.answer()


@router.callback_query(F.data == 'beta_button')
async def beta_button(callback: CallbackQuery):
    await callback.answer('бета кнопка')

@router.callback_query(F.data == 'beta_button_2')
async def beta_button_2(callback: CallbackQuery):
    await callback.answer('бета кнопка')

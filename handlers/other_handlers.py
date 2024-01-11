from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart

from keyboards.keyboard_creator import create_inline_kb
from parser.pars import all_groups, groups_name
from DataBase.db_connect import *

router = Router()


@router.message()
async def delete_message(message: Message):
    await message.delete()

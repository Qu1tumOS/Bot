import asyncio

from aiogram import Bot, Dispatcher, Router
from config.cfg import Config, load_config

from handlers import not_register_handlers
from handlers import start_handlers
from handlers import today_handlers
from handlers import tomorrow_handlers, other_handlers

from handlers.menu_handlers import open_menu_handlers, support_handlers


from handlers.menu_handlers.user_info import info_handlers
from handlers.menu_handlers.user_info import edit_handlers
from handlers.menu_handlers.user_info import delete_handlers
from handlers.menu_handlers.admin_panel import open_panel, update_stat




router = Router()


async def main() -> None:
    print("\n\n ---start--- \n")

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()


    dp.include_router(not_register_handlers.router)

    dp.include_router(start_handlers.router)
    dp.include_router(today_handlers.router)
    dp.include_router(tomorrow_handlers.router)
    dp.include_router(open_menu_handlers.router)
    dp.include_router(info_handlers.router)
    dp.include_router(edit_handlers.router)
    dp.include_router(delete_handlers.router)
    dp.include_router(open_panel.router)
    dp.include_router(support_handlers.router)
    dp.include_router(update_stat.router)

    dp.include_router(other_handlers.router)


    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, skip_updates=False)


if __name__ == '__main__':
    asyncio.run(main())
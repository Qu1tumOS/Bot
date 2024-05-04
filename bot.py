import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, Router
from config.cfg import Config, load_config, Settings

from handlers import not_register_handlers
from handlers import start_handlers
from handlers import today_handlers
from handlers import tomorrow_handlers, other_handlers
from handlers.menu_handlers import open_menu_handlers, support_handlers, money_for_me
from handlers.menu_handlers.user_info import info_handlers
from handlers.menu_handlers.user_info import edit_handlers
from handlers.menu_handlers.user_info import delete_handlers
from handlers.menu_handlers.admin_panel import check_users, open_panel, stats
from handlers.menu_handlers.admin_panel.beta_test import open_test_panel, send_for_all
from excel import add_stat
from parser.tests import lessons_on_groups_add_to_table


router = Router()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] #%(levelname)-8s %(name)s '
           '%(funcName)s:%(lineno)d - %(message)s')

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('logs.txt', encoding='utf8')
file_handler.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] #%(levelname)-8s %(name)s '
           '%(funcName)s:%(lineno)d - %(message)s'))
logger.addHandler(file_handler)

async def main() -> None:
    logger.info("start\n")
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
    dp.include_router(check_users.router)
    dp.include_router(stats.router)
    dp.include_router(money_for_me.router)
    dp.include_router(open_test_panel.router)
    dp.include_router(send_for_all.router)

    dp.include_router(other_handlers.router)

    scheduler = AsyncIOScheduler()

    scheduler.add_job(add_stat,
                      'cron',
                      hour=Settings.add_stats_time[:2],
                      minute=Settings.add_stats_time[3:])

    scheduler.add_job(lessons_on_groups_add_to_table,
                      'cron',
                      hour=Settings.pars_all_group_time[:2],
                      minute=Settings.pars_all_group_time[3:])

    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, skip_updates=False)

if __name__ == '__main__':
    asyncio.run(main())
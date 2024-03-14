from dataclasses import dataclass
from environs import Env


class Settings:
    descript = 'ПМ. ОП. ОГСЭ. ЕН. ОУД.'
    add_stats_time = '23:55'
    pars_all_group_time = '11:10'
    dates_format = '%d.%m.%Y'

@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту

@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))

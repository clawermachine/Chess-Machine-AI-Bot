from dataclasses import dataclass
import os

#
@dataclass
class TgBot:
    token: str

#
@dataclass
class Config:
    tg_bot: TgBot

#
def load_config(path: str | None = None) -> Config:
    with open('config_data/tg_api.txt', 'r') as tg_api:
        token = tg_api.readline()
    return Config(tg_bot=TgBot(token=token))


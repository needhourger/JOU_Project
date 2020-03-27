import nonebot
from nonebot import on_startup

from config import CAN_SEND_PIC
from JOU_bot.libs.sql import *

@on_startup
async def startup():
    await database_init()
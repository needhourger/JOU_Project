#-*- coding=utf-8 -*-
import os
import nonebot
import config

from JOU_bot.libs.sql import *

@nonebot.on_startup()
async def startup():
    await database_init()
    config.CAN_SEND_PIC=await nonebot.get_bot().can_send_image()

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__),"JOU_bot","plugins"),
        "JOU_bot.plugins"
    )
    nonebot.run()
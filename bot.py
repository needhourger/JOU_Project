#-*- coding=utf-8 -*-
import os
import nonebot
import config

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__),"JOU_bot","plugins"),
        "JOU_bot.plugins"
    )
    nonebot.run()
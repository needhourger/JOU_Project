#-*- coding=utf-8 -*-
import nonebot
from nonebot import on_command,CommandSession

@on_command("0",aliases=["帮助","使用帮助","获取帮助"])
async def _(session:CommandSession):
    plugins=list(filter(lambda p: p.name,nonebot.get_loaded_plugins()))

    arg=session.current_arg_text.strip().lower()
    if not arg:
        await session.send(
            '\n'.join(p.name for p in plugins)
        )
        return

    for p in plugins:
        if p.name.lower()==arg:
            await session.send(p.usage)
            
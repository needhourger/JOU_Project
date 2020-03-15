#-*- coding:utf-8 -*-
from JOU_bot.libs.sql import *
from JOU_bot.libs.tail import *
from config import LUCK_DRAW_KEYWORDS
from config import LUCK_DRAW_FILES

from nonebot import NLPSession
from nonebot import permission
from nonebot import on_natural_language

__plugin_name__ = '语言库'
__plugin_usage__ = """
回复相应关键词即可触发(●'◡'●)
"""

@on_natural_language(permission=permission.GROUP)
async def group(session:NLPSession):
    msg=session.msg_text.strip()
    group_id=session.ctx.get("group_id",None)
    user_id=session.ctx.get("user_id",None)
    if not (group_id and user_id):
        return
    res=await group_mag_reply(msg,group_id,user_id)
    if not res:
        return
    res=res+await get_tail()
    await session.send(res)

@on_natural_language(permission=permission.PRIVATE)
async def private(session:NLPSession):
    msg=session.msg_text.strip()
    user_id=session.ctx.get("user_id",None)
    flag=await permission.check_permission(session.bot,session.ctx,permission.PRIVATE_FRIEND)
    if user_id and flag and msg==LUCK_DRAW_KEYWORDS:
        with open(LUCK_DRAW_FILES,"a+",encoding="utf-8") as f:
            f.write("{}\n".format(user_id))
            f.close()
        await session.send("参与抽奖成功！")
    res=await private_msg_reply(msg,user_id)
    if not res:
        return
    res=res+await get_tail()
    await session.send(res)


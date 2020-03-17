#-*- coding:utf-8 -*-
from config import PRINTER_MESSAGE
from config import ARGS_SEP

from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission

__plugin_name__ = '准考证打印'
__plugin_usage__ = """
四六级准考证打印

#打印 [QQ号]

填写资料免费打印四六级准考证，送上门。
"""

@on_command("printer",aliases=("打印","准考证打印","四六级准考证打印"),permission=permission.PRIVATE_FRIEND,only_to_me=False)
async def printer(session:CommandSession):
    user_id=session.get("user_id")
    qq=session.get("qq",prompt="请输入您的QQ号")
    if user_id!=qq:
        await session.send("您输入的QQ号与本账号不符")
        return
    await session.send(PRINTER_MESSAGE)

@printer.args_parser
async def _(session:CommandSession):
    user_id=session.ctx.get("user_id",None)
    if not user_id:
        await session.send("非法用户")
        return
    session.state["user_id"]=str(user_id)
    args=session.current_arg_text.strip().split(ARGS_SEP)
    if len(args)>=1:
        session.state["qq"]=args[0]
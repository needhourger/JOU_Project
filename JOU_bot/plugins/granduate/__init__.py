#-*- coding=utf-8 -*-
from JOU_bot.libs.sql import *

from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission

__plugin_name__ = '寻找研友'
__plugin_usage__ = """
寻找研友

#研友  [目标高校全称] [目标专业全称]

发送“#研友 南京大学 计算机与科学”查询同目标研友信息
"""

@on_command("granduate",aliases=("研友","寻找研友"),permission=permission.PRIVATE_FRIEND)
async def granduate(session:CommandSession):
    school_name=session.get("school_name",prompt="请输入目标高校全称")
    major=session.get("major",prompt="请输入目标专业全称")
    user_id=session.get("user_id")
    res=await handle_granduate_data(school_name,major,user_id)
    await session.send(res)


@granduate.args_parser
async def _(session:CommandSession):
    user_id=session.ctx.get("user_id",None)
    if not user_id:
        session.finish("非法用户")
        return
    session.state["user_id"]=user_id
    args=session.current_arg_text.strip().split()
    if len(args)>=2:
        session.state["school_name"]=args[0]
        session.state["major"]=args[1]
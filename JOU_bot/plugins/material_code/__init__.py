#-*- coding=utf-8 -*-
from JOU_bot.libs.sql import *
from config import MATERIAL_GROUP


from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission

__plugin_name__ = '密码'
__plugin_usage__ = r"""
获取下载的学习资料的密码

\#密码
"""

@on_command("material_code",aliases=("密码"),permission=permission.GROUP)
async def material_code(session:CommandSession):
    user_id=session.get("user_id",prompt="非法的发送者")
    ret=await get_material_record(user_id)
    await session.send(ret)

@material_code.args_parser
async def _(session:CommandSession):
    group_id=session.ctx.get("group_id",None)
    if not group_id or group_id==MATERIAL_GROUP:
        session.finish("请在群{}发送“#密码”命令".format(MATERIAL_GROUP))
    user_id=session.ctx.get("user_id",None)
    if not user_id:
        session.finish("非法的发送者")
    session.state["user_id"]=user_id



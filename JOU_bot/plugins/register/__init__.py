#-*- coding=utf-8 -*-
from JOU_bot.libs.sql import *

from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission

import re


__plugin_name__ = '认证'
__plugin_usage__ = r"""
实名认证

\#认证  [学号] [身份证后八位]

注册认证你校园门户的账号
"""

@on_command("register",aliases=("认证","注册"),permission=permission.PRIVATE_FRIEND)
async def register(session:CommandSession):
    username=session.get("username",prompt="请输入学号信息")
    password=session.get("password",prompt="请输入密码：默认身份证后八位")
    qq=session.get("qq",prompt="非法的发送者")
    ret=await saveUserInfo(username,password,qq)
    await session.send(ret)


@register.args_parser
async def _(session:CommandSession):
    qq=session.ctx.get("user_id",None)
    if not qq:
        session.finish("非法的发送者")
    session.state["qq"]=qq
    args=session.current_arg_text.strip().split()
    if not args or len(args)<2:
        session.pause(__plugin_usage__)
    session.state["username"]=args[0]
    session.state["password"]=args[1]
    


    

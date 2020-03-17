#-*- coding=utf-8 -*-
from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission

__plugin_name__ = '留言'
__plugin_usage__ = """
留言功能

#留言 [留言内容]

留言参与各式各样的精彩活动
"""

@on_command("leave_message",aliases=("留言"),permission=permission.PRIVATE_FRIEND,only_to_me=False)
async def leave_message(session:CommandSession):
    message=session.get("message",prompt="请输入你的留言内容")
    with open("./留言.txt","a+",encoding="utf-8") as f:
        f.write(message+"\n")
        f.close()
    await session.send("留言成功")
    

@leave_message.args_parser
async def _(session:CommandSession):
    msg=session.current_arg_text.strip()
    if msg:
        session.state["message"]=session.current_arg_text.strip()
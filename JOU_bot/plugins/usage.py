# #-*- coding=utf-8 -*-
# from config import ARGS_SEP
# import nonebot
# from nonebot import on_command,CommandSession

# @on_command("0",aliases=["帮助","使用帮助","获取帮助"],only_to_me=False)
# async def _(session:CommandSession):
#     plugins=list(filter(lambda p: p.name,nonebot.get_loaded_plugins()))

#     arg=session.current_arg_text.strip().lower()
#     if not arg:
#         msg="[CQ:emoji,id=10084] 功能列表 [CQ:emoji,id=10084]\n"
#         for p in plugins:
#             msg+="[CQ:emoji,id=10004]  "+p.name+"\n"
#         msg+="回复“#帮助 [功能名称]”查看帮助详情"
#         await session.send(msg)
#         return

#     for p in plugins:
#         if p.name.lower()==arg:
#             await session.send(p.usage)
            
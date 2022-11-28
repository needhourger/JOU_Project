import re
from nonebot import Bot, on_command, on_message
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent,Message,MessageSegment

from src.libs import getSaying

from src.database import getReply

kr = on_message(priority=100,rule=to_me(),block=True)

@kr.handle()
async def kr_handle(bot:Bot, event:MessageEvent|GroupMessageEvent):
    msg = event.get_message().extract_plain_text()
    msg = re.sub(r"\[.*?\]","",msg)

    if not msg or msg.isspace():
        return

    if isinstance(event,GroupMessageEvent):
        nickname = event.sender.card or event.sender.nickname
        fromId = event.group_id
    else:
        nickname = event.sender.nickname
        fromId = event.sender.user_id

    reply = await getReply(fromId,msg)
    print(reply)
    if not reply:
        return
    saying = await getSaying()
    retMessage = Message(reply+"\n{}\n".format(saying)+bot.config.bot_tail)
    await kr.finish(retMessage)
    

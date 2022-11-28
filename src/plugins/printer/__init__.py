from nonebot import Bot,on_notice,get_driver
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.event import NoticeEvent
from nonebot.adapters.onebot.v11 import Message

from src.database.models import Prints

printer = on_notice(priority=100,rule=to_me,block=True)

@printer.handle()
async def printer_handle(bot:Bot,event:NoticeEvent):
    j = event.dict()
    # print(j)
    if (j.get("notice_type",None) != "offline_file"):
        printer.finish()

    if (not j["file"]["name"].endswith(".pdf")):
        printer.finish()

    prints = Prints(uid=j["user_id"],url=j["file"]["url"],name=j["file"]["name"])
    # print(prints)
    try:
        prints.save(force_insert=True)
    except:
        prints.save()

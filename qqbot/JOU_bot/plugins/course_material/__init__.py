#-*- coding=utf-8 -*-
from JOU_bot.libs.sql import *
from JOU_bot.libs.qr import *
from JOU_bot.libs.html import *
from config import PASSWORD_SEED
from config import HTTP_ROOT
from config import HTTP_URL_PRIFX
from config import MATERIAL_GROUP
from config import IMAGE_SAVE_PATH
from config import ARGS_SEP
from config import CAN_SEND_PIC

from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission

import os
import random
import string
import subprocess

__plugin_name__ = '学习资料'
__plugin_usage__ = """
获取学习资料

#资料 [资料编号]

单独回复“资料”查看资料编号列表
"""

@on_command("course_material",aliases=("资料","学习资料"),permission=permission.PRIVATE_FRIEND,only_to_me=False)
async def course_material(session:CommandSession):
    material_id=session.get("material_id")
    qq=session.get("qq")
    filepath=await material_path_query(material_id)
    if not filepath:
        await session.send("未查询到相关资料")
        return
    filename=os.path.split(filepath[0])[-1]+".zip"
    savepath=os.path.join(HTTP_ROOT,qq,filename)
    password=generate_password(PASSWORD_SEED)
    await record_material_password(qq,filename,password)
    await generate_QR_code(HTTP_URL_PRIFX+qq,os.path.join(IMAGE_SAVE_PATH,qq))
    await generate_html(os.path.join(HTTP_ROOT,qq))
    await session.send("文件已打包完成，压缩文件密码请到群{}发送“#密码”获取".format(MATERIAL_GROUP))
    if not CAN_SEND_PIC:
        await session.send("无法发送图片")
        return
    await session.send("[CQ:image,file={}]".format(qq+"/QRcode.png"))
    subprocess.Popen(["7za.exe","a","-tzip",savepath,"-p"+password,filepath])


@course_material.args_parser
async def _(session:CommandSession):
    qq=session.ctx.get("user_id",None)
    if not qq:
        session.finish("非法的发送者")
        return
    session.state["qq"]=str(qq)
    args=session.current_arg_text.strip().split(ARGS_SEP)
    if not args:
        session.pause(__plugin_usage__)
    session.state["material_id"]=args[0]

def generate_password(seed):
    return seed+"".join(random.sample(string.ascii_letters+string.digits,8))
    
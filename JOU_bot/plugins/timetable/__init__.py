from config import DATABASE_PATH
from config import IMAGE_SAVE_PATH
from config import CHROME_BINARY
from config import WEBDRIVE_PATH
from JOU_bot.libs.sql import *

import nonebot
from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission

import os
from selenium import webdriver

__plugin_name__="课表"
__plugin_usage__=r"""
获取课程表

\#课表
\#课表 [学号] [身份证后八位]

校园门户的登陆中行号密码
"""

@on_command("timetable",aliases=("课表","课程表"),permission=permission.PRIVATE_FRIEND)
async def timetable(session:CommandSession):
    username=session.get("username",prompt="请输入学号信息")
    password=session.get("password",prompt="请输入密码：默认身份证后八位")
    qq=session.get("qq",prompt="非法的发送者")
    ret=await handle(username,password,qq)
    if not session.bot.can_send_image():
        await session.send("无法发送图片")
    await session.send(ret)

@timetable.args_parser
async def _(session:CommandSession):
    qq=session.ctx.get("user_id",None)
    if not qq:
        session.finish("非法发送者")
    session.state["qq"]=qq
    args=session.current_arg_text.strip().split()
    if not args:
        session.pause(__plugin_usage__)
    if len(args)==0:
        res=await getUserPass(qq)
        if not res:
            session.state["username"],session.state["password"]=res
        else:
            return
    elif len(args)==2:
        session.state["username"]=args[0]
        session.state["password"]=args[1]

async def handle(username:str,password:str,qq:str)->str:
    url=r"https://cas.hhit.edu.cn/lyuapServer/login?service=http://58.192.29.7/login_cas.aspx"

    options=webdriver.ChromeOptions()
    options._binary_location=CHROME_BINARY
    options.add_argument("--disable_gpu")
    options.add_argument("--allow_running-inecure-content")
    options.add_argument("--disable-extensions")

    chrome=webdriver.Chrome(chrome_options=options,executable_path=WEBDRIVE_PATH)
    chrome.get(url)
    chrome.find_element_by_id("username").send_keys(username)
    chrome.find_element_by_id("password").send_keys(password)
    chrome.find_element_by_class_name("btn-submit").click()

    URL=chrome.find_element_by_xpath("""//*[@id="headDiv"]/ul/li[5]/ul/li[1]/a""").get_attribute("href")
    # print(URL)
    chrome.get(URL)
    body=chrome.find_element_by_xpath("/html/body")
    width=body.size['width']
    height=body.size['height']
    chrome.set_window_size(width,height)
    savepath=os.path.join(IMAGE_SAVE_PATH,qq)
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    chrome.save_screenshot(savepath+"/school_timetable.jpg")
    return "[cq:image,file={}]".format(qq+"/school_timetable.jpg")
from config import DATABASE_PATH
from config import IMAGE_SAVE_PATH
from config import CHROME_BINARY
from config import WEBDRIVE_PATH
from config import DEBUG
from config import ARGS_SEP
from config import CAN_SEND_PIC
from JOU_bot.libs.sql import *

import nonebot
from nonebot import on_command
from nonebot import CommandSession
from nonebot import permission
from nonebot.command.argfilter.controllers import handle_cancellation

import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

__plugin_name__="查询课表"
__plugin_usage__="""
获取课程表

#课表
#课表 [学号] [身份证后八位]

校园门户的登陆中行号密码
如果您已经完成身份认证则可以直接发送“#课表”
"""

@on_command("timetable",aliases=("课表","课程表","查询课表","查询课程表"),permission=permission.PRIVATE_FRIEND,only_to_me=False)
async def timetable(session:CommandSession):
    username=session.get("username",prompt="请输入学号信息")
    password=session.get("password",prompt="请输入密码：默认身份证后八位")
    qq=session.get("qq")
    await session.send("尝试获取课程表中···")
    ret=await handle(username,password,qq)
    if not CAN_SEND_PIC:
        await session.send("无法发送图片")
        return
    await session.send(ret)

@timetable.args_parser
async def _(session:CommandSession):
    qq=session.ctx.get("user_id",None)
    if not qq:
        session.finish("非法发送者")
    session.state["qq"]=str(qq)
    args=session.current_arg_text.strip().split(ARGS_SEP)
    await session.send(session.current_arg_text)
    if len(args)==0:
        res=await getUserPass(qq)
        if res:
            session.state["username"],session.state["password"]=res
            return
        else:
            await session.send("您未完成认证，没有记录您的账号密码\n")
            return
    elif len(args)==1:
        session.state["username"]=args[0]
    elif len(args)>=2:
        session.state["username"]=args[0]
        session.state["password"]=args[1]


async def handle(username:str,password:str,qq:str)->str:
    url=r"https://cas.hhit.edu.cn/lyuapServer/login?service=http://58.192.29.7/login_cas.aspx"

    options=webdriver.ChromeOptions()
    options._binary_location=CHROME_BINARY
    options.add_argument("--disable_gpu")
    options.add_argument("--allow_running-inecure-content")
    options.add_argument("--disable-extensions")
    if not DEBUG:
        options.add_argument("--headless")

    chrome=webdriver.Chrome(chrome_options=options,executable_path=WEBDRIVE_PATH)
    chrome.get(url)
    chrome.find_element_by_id("username").send_keys(username)
    chrome.find_element_by_id("password").send_keys(password)
    chrome.find_element_by_class_name("btn-submit").click()

    try:
        URL=chrome.find_element_by_xpath("""//*[@id="headDiv"]/ul/li[5]/ul/li[1]/a""").get_attribute("href")
    except NoSuchElementException:
        chrome.quit()
        return "学号或者密码错误"
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
    chrome.quit()
    return "[CQ:image,file={}]".format(qq+"/school_timetable.jpg")
#-*- coding:utf-8 -*-
import os
import logging
from libs import *

from message import Message
WORKAREA,_=os.path.split(os.path.abspath(__file__))


config=loadConfig()
file_list=loadFileList(config)
for f in file_list:
    t=processFile(f,config)
    if t:
        file_list.remove(t)
        os.remove(t)


print("\n>> 格式问题未能处理的文件列表如下:")
for f in file_list:
    print(f)
input("按回车键结束")
    
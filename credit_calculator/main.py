#-*- coding:utf-8 -*-
import os
import logging
from libs import *

from message import Message
WORKAREA,_=os.path.split(os.path.abspath(__file__))


config=loadConfig()
file_list=loadFileList(config)
for f in file_list:
    processFile(f,config)

input("按回车键结束")
    
#-*- coding=utf-8 -*-
import sqlite3
import os
import sys

DATABASE="./CQtest.db"
# DATABASE="./CQtest.db"
SETTING="./setting"
logo=r"""

   __________  __            __     __  ___                                 
  / ____/ __ \/ /____  _____/ /_   /  |/  /___ _____  ____ _____ ____  _____
 / /   / / / / __/ _ \/ ___/ __/  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ ___/
/ /___/ /_/ / /_/  __(__  ) /_   / /  / / /_/ / / / / /_/ / /_/ /  __/ /    
\____/\___\_\__/\___/____/\__/  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/     
                                                         /____/             

"""

def Menu(menu_type):
    os.system("cls")
    print(logo)
    print(menu_type)
    choice=input(">请输入你的选择: ")
    return choice


def vip_Manager():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    while True:
        c.execute("select QQ_ID from Users where isVIP=1;")
        os.system("cls")
        print("========VIP列表========")
        for row in c:
            print(row[0])
        print("===命令：add del exit===")
        choice=""
        choice=input(">cmd: ")
        if choice=="add":
            choice=input("QQ：")
            try:
                c.execute("update Users set isVIP=1 where QQ_ID={};".format(choice))
                conn.commit()
            except:
                print("增加失败,可能该用户不存在，请先让用户完成认证注册")
                os.system("pause")

        elif choice=="del":
            choice=input("QQ：")
            try:
                c.execute("update Users set isVIP=0 where QQ_ID={};".format(choice))
                conn.commit()
            except:
                print("删除失败")
                os.system("pause")
        elif choice=="exit":
            break
    conn.close()


def lang_Manager():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    while True:
        c.execute("select ID,Priority,isON,keyword,ReplyType,Reply from Languages order by ID;")
        os.system("cls")
        print("=========语言库列表=========")
        for row in c:
            print("=====================================================")
            print("{}#\t优先级：{}\t是否启用：{}\t关键词：{}\t回复对象：{}\n回复：{}".format(row[0],row[1],"是" if row[2]==1 else "否",row[3],row[4],row[5]))
            print("=====================================================")
        print(
            "==========\n"
            "命令：add del switch exit\n"
            "注意:回复对象：0:不限制用户|1:所有私聊|2:所有群聊\n"
            "     群号:固定群|QQ:固定用户\n"
            "群号，QQ必须存在于应答群列表，基础用户列表中\n"
            "回复对象默认：0所有用户\n"
            "==========\n"
        )
        choice=""
        choice=input(">cmd: ")
        if choice=="add":
            key=input("关键词：")
            reply=input("回  复：")
            try:
                p=int(input("优先级："))
            except:
                p=99
            
            try:
                ReplyType=int(input("回复对象："))
            except:
                ReplyType=0
            
            # print("{} {} {}".format(key,reply,p))
            try:
                c.execute("insert into languages (keyword,Reply,priority,ReplyType) values ('{}','{}',{},{});".format(key,reply,p,ReplyType))
                conn.commit()
            except:
                print("插入，请检查关键词是否有误")
                os.system("pause")

        elif choice=="del":
            choice=input("需要删除的数据的编号：")
            try:
                c.execute("delete from languages where ID={};".format(choice))
                conn.commit()
            except:
                print("删除失败，请检查您的输入编号是否正确")
                os.system("pause")

        elif choice=="switch":
            choice=input("请输入需要启用或关闭的编号：")
            c.execute("select isON from languages where ID={};".format(choice))
            row=c.fetchone()
            # print(row)
            if row==None:
                print("输入的编号不存在数据库中")
                os.system("pause")
            else:
                if row==(1,):
                    c.execute("update languages set isON=0 where ID={};".format(choice))
                    conn.commit()
                elif row==(0,):
                    c.execute("update languages set isON=1 where ID={};".format(choice))
                    conn.commit()
                else:
                    print("切换失败")
                    os.system("pause")
        elif choice=="exit":
            break
    conn.close()



def blacklist_Manager():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    while True:
        c.execute("select QQ_ID from Users where isBanned=1;")
        os.system("cls")
        print("========黑名单列表========")
        for row in c:
            print(row[0])
        print("===命令：add del exit===")
        choice=""
        choice=input(">cmd: ")
        if choice=="add":
            choice=input("QQ：")
            try:
                c.execute("update Users set isBanned=1 where QQ_ID={};".format(choice))
                conn.commit()
            except:
                print("增加失败,可能该用户未完成认证注册不存在")
                os.system("pause")

        elif choice=="del":
            choice=input("QQ：")
            try:
                c.execute("update Users set isBanned=0 where QQ_ID={};".format(choice))
                conn.commit()
            except:
                print("删除失败，可能该用户不存在")
                os.system("pause")
        elif choice=="exit":
            break
    conn.close()
           

def notice_Manager():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    while True:
        c.execute("select ID,item,campus,uptime,QQ_ID,detail from Notices;")
        os.system("cls")
        print("========================失物招领信息表===========================")
        for row in c:
            print("======================================================================")
            print("{}# 物品：{}\t校区：{}\t时间：{}\tQQ:{}\n详情：{}".format(row[0],row[1],row[2],row[3],row[4],row[5]))
            print("======================================================================")
        print("==命令：del exit==")
        choice=""
        choice=input(">cmd: ")
        if choice=="del":
            choice=input("请输入信息编号：")
            try:
                c.execute("delete from Notices where ID={};".format(choice))
                conn.commit()
            except:
                print("删除失败，请检查你输入的编号")
                os.system("pause")
        elif choice=="exit":
            break
    conn.close()

def groups_Manager():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    while True:
        c.execute("select groupid from groups order by ID;")
        os.system("cls")
        print("========应答群列表========")
        for row in c:
            print(row[0])
        print("====命令：add del exit====")
        print("注意：0,1,2被删除将导致无法使用语言库的三种大类回复")
        choice=""
        choice=input(">cmd: ")
        if choice=="add":
            choice=input("群号：")
            try:
                c.execute("insert into groups (groupID) values ({});".format(choice))
                conn.commit()
            except:
                print("插入失败，你输入的数据有误")
                os.system("pause")
        elif choice=="del":
            choice=input("群号：")
            try:
                c.execute("delete from groups where groupID={};".format(choice))
                conn.commit()
            except:
                print("删除失败，请检查群号")
                os.system("pause")
        elif choice=="exit":
            break
    conn.close()
        

def users_Manager():
    pass

def setting_Manager():
    with open(SETTING,"r",encoding="utf-8") as f:
        lines=f.readlines()
        SAVE_PATH=lines[0]
        URL_BASE=lines[1]
        SUFFIX=lines[2]
        print("==============基础设置================")
        print("下载文件保存目录：{}".format(SAVE_PATH))
        print("网页链接基础链接：{}".format(URL_BASE))
        print("音乐文件后缀：{}".format(SUFFIX))
        print("======================================")
        print(
            "以上设置仅供预览，请到目录下setting文件修改\n"
            "修改之后需要重启酷Q方可生效"
        )
        f.close()
        return
    print("无法读取基础设置文件，请检查文件目录完整性")
    os.system("pause")


menu0="""
============================================================================
=                              1.VIP用户管理                                =
=                              2.黑名单管理                                 =
=                              3.语言库管理                                 =
=                              4.失物招领信息管理                           =
=                              5.答复群管理                                 =
=                              exit 退出                                    =
============================================================================
注意：请勿在任何时候强行关闭命令行，请使用exit返回上级菜单或者退出防止数据错误
============================================================================
"""


def main():
    while (True):
        choice=Menu(menu0)
        if choice=="":
            continue
        if choice[0]=='1':
            vip_Manager()
        elif choice[0]=='2':
            blacklist_Manager()
        elif choice[0]=='3':
            lang_Manager()
        elif choice[0]=='4':
            notice_Manager()
        elif choice[0]=='5':
            groups_Manager()
        # elif choice[0]=='6':
        #     setting_Manager()
        # elif choice[0]=='0':
        #     users_Manager()
        elif choice=="exit":
            return


if __name__=="__main__":
    main()



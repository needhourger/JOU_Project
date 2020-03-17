#-*- coding=utf-8 -*-
from config import DATABASE_PATH
from config import GRANDUATE_MESSAGE
import sqlite3

db=sqlite3.connect(DATABASE_PATH)
if not db:
    raise "无法连接数据库"
cursor=db.cursor()

users_sql="""
CREATE TABLE IF NOT EXISTS Users(
QQ_ID INTEGER PRIMARY KEY NOT NULL,
Stu_ID INTEGER,
Password TEXT,
Name TEXT DEFAULT NULL,
Gender TEXT DEFAULT NULL,
Department TEXT DEFAULT NULL,
Notice_uptime TEXT DEFAULT NULL,
isVIP INTEGER DEFAULT 0,
isBanned INTEGER DEFAULT 0,
isRegistered INTEGER DEFAULT 0
);
"""

granduate_sql="""
create table if not exists granduate(
    user_id integer primary key not null,
    school_name text default null,
    major text default null
)
"""
        

async def saveUserInfo(username:str,password:str,qq:int)->str:
    info={}
    cursor.execute(users_sql)
    db.commit()
    cursor.execute("select isBanned,isRegistered from users where Stu_id={} limit 1;".format(username))
    row=cursor.fetchone()
    if row is None or row==(0,0):
        cursor.execute("insert or replace into users (QQ_ID,Stu_ID,Password,Name,Gender,Department,Notice_uptime,isvip,isbanned,isregistered) values({},{},'{}','{}','{}','{}',NULL,0,0,1);".format(qq,username,password,info.get('姓名',""),info.get('性别',""),info.get('部门',"")))
    db.commit()
    return "认证成功"

async def getUserPass(qq):
    cursor.execute("""
    select Stu_ID,Password from users where QQ_ID={}
    """.format(qq))
    return cursor.fetchone()

async def material_path_query(material_id):
    cursor.execute("""
    select path from material where NO={}
    """.format(material_id))
    return cursor.fetchone()

async def record_material_password(user_id,filename,password):
    cursor.execute("insert into material_record (material,password,qq_belong,uptime) values (?,?,?,datetime())",(filename,password,user_id))
    db.commit()
    return

async def get_material_record(qq):
    ret=""
    cursor.execute("select material,password from material_record where qq_belong={}".format(qq))
    res=cursor.fetchall()
    for row in res:
        ret+="压缩包名:{} 密码：{}\n".format(row[0],row[1])
    if not ret:
        return "未查询过到您有尝试获取过学习资料"
    return ret

async def group_mag_reply(msg,group_id,user_id):
    cursor.execute("select keyword,reply from languages where replyType=0 or replyType=2 or replyType={} and isON=1 order by Priority desc".format(group_id))
    rows=cursor.fetchall()
    for row in rows:
        if len(row)>=2 and row[0] in msg:
            return row[1]

async def private_msg_reply(msg,user_id):
    cursor.execute("select keyword,reply from languages where replyType=0 or replyType=1 or replyType={} and isON=1 order by priority desc".format(user_id))
    rows=cursor.fetchall()
    for row in rows:
        if len(row)>=2 and row[0] in msg:
            return row[1]

async def handle_granduate_data(school_name,major,user_id):
    cursor.execute(granduate_sql)
    db.commit()
    ret="为您查询到研友信息如下:\n"
    cursor.execute("insert or replace into granduate (school_name,major,user_id) values (?,?,?)",(school_name,major,user_id))
    cursor.execute("select school_name,major,user_id from granduate where school_name=? and user_id!=?",(school_name,user_id))
    rows=cursor.fetchall()
    for row in rows:
        ret+="{} - {}\t{}".format(row[0],row[1],row[2])
    if ret=="为您查询到研友信息如下:\n":
        ret="未能查询到同校研友\n"
    ret+=GRANDUATE_MESSAGE
    return ret

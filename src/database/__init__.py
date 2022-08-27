from .models import KeyReply, User,db

def database_init():
    db.connect()
    db.create_tables([KeyReply,User])
    # test = KeyReply(keyword="测试",reply="测试结果")
    # test.save()
    # admin = User(username="test",password="test")
    # admin.save()

async def getReply(sender_id:int,key:str):
    replys = KeyReply.select().where(
        (KeyReply.keyword == key) & 
        ((KeyReply.target == 0) | (KeyReply.target == sender_id)) &
        (KeyReply.enabled)).order_by(KeyReply.priority)
    # print(replys)
    if not replys:
        return None
    return replys[0].reply

async def admin_login(username:str,password:str)->bool:
    user = User.select().where((User.username == username) & (User.password == password)).limit(1)
    print(user)
    if not user:
        return False
    return True

async def getAllReplys():
    replys = KeyReply.select().order_by(KeyReply.created)
    return replys

async def addReply(keyword,reply,target,priority):
    kr = KeyReply(keyword=keyword,reply=reply,target=target,priority=priority)
    kr.save()

async def deleteKeyReply(kid):
    KeyReply.delete().where(KeyReply.kid==kid).execute()
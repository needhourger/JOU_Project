import os
from nonebot import get_driver
from nonebot.drivers import ReverseDriver
from fastapi import FastAPI, File,Request,Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse

from src.database import addReply, admin_login, deleteKeyReply, getAllReplys


driver = get_driver()

if not isinstance(driver, ReverseDriver) or not isinstance(driver.server_app, FastAPI):
    raise ValueError("Dashboard supports FastAPI driver only")

app = driver.server_app
app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/dashboard/login")
async def dashboard_login(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})


@app.post("/dashboard/login")
async def login(username:str=Form(),password:str=Form()):
    flag = await admin_login(username,password)
    if not flag:
        return RedirectResponse(url="/dashboard/login",status_code=303)
    return RedirectResponse("/dashboard",status_code=303)

@app.get("/dashboard")
async def dashboard(request:Request):
    krs = await getAllReplys()
    return templates.TemplateResponse("dashboard.html",{"request":request,"krs":krs})

@app.post("/dashboard/addKeyReply")
async def dashboard_add_key_reply(formfile:UploadFile=File(default=None),keyword:str=Form(),reply:str=Form(),target:int=Form(),priority:int=Form()):
    await addReply(keyword,reply,target,priority)
    if formfile:
        data = await formfile.read()
        filename = formfile.filename
        with open(os.path.join("./data/image",filename)) as f:
            f.write(data)
            f.close() 
    return RedirectResponse("/dashboard",status_code=303)
    

@app.get("/dashboard/deleteKeyReply")
async def dashboard_delete_key_reply(kid=None):
    # print(kid)
    if kid:
       await deleteKeyReply(kid)
    return RedirectResponse("/dashboard",status_code=303)

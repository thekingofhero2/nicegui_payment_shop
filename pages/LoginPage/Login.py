from pathlib import Path

from typing import Optional
from fastapi import Depends
from fastapi.responses import RedirectResponse
from hashlib import md5
from nicegui import Client, app, ui
import DB.Models as Models 
from DB.CRUD import *
from settings import get_db
import time


        
def page_init():
    ui.add_css("""
:root {
               background:
radial-gradient(rgba(255,255,255,0) 0, rgba(255,255,255,.15) 30%, rgba(255,255,255,.3) 32%, rgba(255,255,255,0) 33%) 0 0,
radial-gradient(rgba(255,255,255,0) 0, rgba(255,255,255,.1) 11%, rgba(255,255,255,.3) 13%, rgba(255,255,255,0) 14%) 0 0,
radial-gradient(rgba(255,255,255,0) 0, rgba(255,255,255,.2) 17%, rgba(255,255,255,.43) 19%, rgba(255,255,255,0) 20%) 0 110px,
radial-gradient(rgba(255,255,255,0) 0, rgba(255,255,255,.2) 11%, rgba(255,255,255,.4) 13%, rgba(255,255,255,0) 14%) -130px -170px,
radial-gradient(rgba(255,255,255,0) 0, rgba(255,255,255,.2) 11%, rgba(255,255,255,.4) 13%, rgba(255,255,255,0) 14%) 130px 370px,
radial-gradient(rgba(255,255,255,0) 0, rgba(255,255,255,.1) 11%, rgba(255,255,255,.2) 13%, rgba(255,255,255,0) 14%) 0 0,
linear-gradient(45deg, #343702 0%, #184500 20%, #187546 30%, #006782 40%, #0b1284 50%, #760ea1 60%, #83096e 70%, #840b2a 80%, #b13e12 90%, #e27412 100%);
background-size: 470px 470px, 970px 970px, 410px 410px, 610px 610px, 530px 530px, 730px 730px, 100% 100%;
background-color: #840b2a;
               }
               """)






@ui.page('/login')
def login(db:Session = Depends(get_db)) -> Optional[RedirectResponse]:
    ui.page_title("登录")
    page_init()
    async def try_login() -> None:  # local function to avoid passing username and password as arguments
        check_res = check_pwd(db=db,uname = username.value,pwd=md5(password.value.encode("utf-8")).hexdigest())
        if check_res is not None:
            app.storage.user['authenticated'] = True
            app.storage.user["username"] = username.value
            app.storage.user["uid"] = check_res
            ui.navigate.to('/')
        else:
            ui.notify("用户名或密码错误",type='negative')
    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.row().classes("w-full items-stretch absolute-center justify-center"):
        with ui.card().classes("items-stretch login-card col-span-8 inset-shadow-down ").style("""
                                                        gap: 20px;
                                                        border-radius: 10px;
                                                        backdrop-filter: blur(19px);
                                                        background-color: rgba(0,191,255, 0.146);
                                                        box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px;
                                                        border: 2px rgba(255,255,255,0.4) solid;
                                                        border-bottom: 2px rgba(40,40,40,0.35) solid;
                                                        border-right: 2px rgba(40,40,40,0.35) solid;
                                                                                               """):
            ui.label("欢迎登录！").classes("text-h5 text-center  text-grey-1 ")
            username = ui.input('账号').on('keydown.enter', try_login).props("""outlined rounded dark""").classes(" ")
            password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login).props("outlined rounded dark").classes(" ")
            ui.button('登录', on_click=try_login)
            ui.space()
            ui.markdown()
        #with ui.column().classes("col-span-7"):
        ui.image("./assets/login.jpg").props(""" width=15% """).classes("inset-shadow-down ")
    with ui.footer():
        ui.label("background css is from https://projects.verou.me/css3patterns/#rainbow-bokeh")
    return None




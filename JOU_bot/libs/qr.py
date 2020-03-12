#-*- coding=utf-8 -*-
import os
import qrcode

async def generate_QR_code(data:str,savePath:str):
    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )
    qr.add_data(data)
    qr.make(fit=True)

    img=qr.make_image(fill_color="black",back_color="white")
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    img.save(savePath+"/QRcode.png")

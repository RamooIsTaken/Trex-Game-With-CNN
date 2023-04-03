import keyboard
import uuid
import time 
from PIL import Image
from mss import mss #mss kütüphanesi koordinatlar doğrultuusnra ekranı kesip frame haline getiren kütüphane
import os

"""https://www.trex-game.skipser.com/"""

mon = { "top": 435, "left": 700, "width": 500, "height": 160}
sct = mss()
i=0
isExit = False

if not os.path.exists("./img/"):
    os.makedirs("./img/")


def recordScreen(recordId,key):
    global i
    i += 1
    print("{}: {}".format(key,i)) #key basılan tuş , i kaç kez basıldığı
    img = sct.grab(mon)
    im =Image.frombytes("RGB",img.size,img.rgb)
    im.save("./img/{}_{}_{}.png".format(key,recordId,i))


def exit():
    global isExit
    isExit = True

keyboard.add_hotkey("esc",exit)
recordId = uuid.uuid4()

while True :
    if isExit: break

    try :
        if keyboard.is_pressed(keyboard.KEY_UP):
            recordScreen(recordId,"up")
            time.sleep(0.1)
        elif keyboard.is_pressed(keyboard.KEY_DOWN):
            recordScreen(recordId,"down")
            time.sleep(0.1)
        elif keyboard.is_pressed("right"):
            recordScreen(recordId,"right")
            time.sleep(0.1)
    except RuntimeError : continue










from keras.models import model_from_json
import numpy as np
from PIL import Image
import keyboard
import time
from mss import mss


mon = { "top": 435, "left": 700, "width": 500, "height": 160}
sct = mss()
width = 125
height = 50

#model yükle
model = model_from_json(open("trexWeigh.json","r").read())
model.load_weights("trexWeigh.h5")


# down=0 ,right=1 ,up=2
labels = ["Down","Right","Up"]

frameRateTime = time.time()
counter = 0
i=0
delay=0.4
keyDownPressed = False




while True :
    #ekran görüntüsü alma
    img = sct.grab(mon)
    im = Image.frombytes("RGB",img.size,img.rgb)
    im2 = np.array(im.convert("L").resize((width,height)))
    im2 = im2 / 255

    X = np.array([im2])
    X = X.reshape(X.shape[0],width,height,1)
    r = model.predict(X)

    result = np.argmax(r)


    if result == 0 : #down = 0
        keyDownPressed = True
    elif result == 2 : # up = 2
        keyboard.press(keyboard.KEY_DOWN)

        if keyDownPressed :
            keyboard.release(keyboard.KEY_DOWN)
        time.sleep(delay)
        keyboard.press(keyboard.KEY_UP)

        if i < 1500 :
            time.sleep(0.3)
        elif 1500<i and i>5000:
            time.sleep(0.2)
        else : time.sleep(0.17)

    keyboard.press(keyboard.KEY_DOWN)
    keyboard.release(keyboard.KEY_DOWN)

    counter +=1

    if (time.time() - frameRateTime) > 1 :
        counter = 0
        frameRateTime = time.time()

        if i < 1500 :
            delay -= 0.003
        else :
            delay -=0.005
        if delay < 0 :
            delay = 0

        print("------------------------------")
        print("Down: {} \nRight: {}\nUp: {} \n".format(r[0][0],r[0][1],r[0][2]))
        i += 1






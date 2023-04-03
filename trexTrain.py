import glob #Resim ve klasörde gezme
import os
import numpy as np
from keras.models import Sequential  #keras derin öğrenme
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D
from PIL import Image
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

def oneHotLabels(values):
    labelEncoder = LabelEncoder()
    integerEncoded = labelEncoder.fit_transform(values)
    oneHotEncoder = OneHotEncoder(sparse=False)
    integerEncoded = integerEncoded.reshape(len(integerEncoded),1)
    oneHotEncoded = oneHotEncoder.fit_transform(integerEncoded)
    return oneHotEncoded
    


imgs = glob.glob("./img/*.png")
width = 125
height = 50

X = [] #resimleri tutmak içi
Y = [] #labelları tutmak için 

for img in imgs :
    filename = os.path.basename(img)
    label = filename.split("_")[0] #ilk etiket hangi tuşa basıldığını gösteriyor
    im = np.array(Image.open(img).convert("L").resize((width,height)))
    im = im / 255 #normalize için
    X.append(im)
    Y.append(label)

X = np.array(X)
X = X.reshape(X.shape[0],width,height,1) # 1 yazılmasının nedeni siyah beyaz olarak saklamak
Y  = oneHotLabels(Y)

trainX,testX,trainY,testY = train_test_split(X,Y,test_size=0.25,random_state=2)

model = Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation="relu",input_shape=(width,height,1))) #input shape sadece giriş katmanında versek kafii
model.add(Conv2D(64,kernel_size=(3,3),activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128,activation="relu"))
model.add(Dropout(0.4))
model.add(Dense(3,activation="softmax")) # çıkış katmanı


model.compile(loss="categorical_crossentropy",optimizer="Adam",metrics=["accuracy"])
model.fit(trainX,trainY,epochs=40,batch_size=64)

scoreTrain = model.evaluate(trainX,trainY)# ilk indeks kaybı, ikinci indeks accuracy verir
print("Eğitim doğruluğu :",scoreTrain[1]*100)

scoreTest = model.evaluate(testX,testY)
print("Test doğruluğu :",scoreTest[1]*100)

#modeli kaydetmek için
open("trexWeigh.json","w").write(model.to_json())
model.save_weights("trexWeigh.h5")




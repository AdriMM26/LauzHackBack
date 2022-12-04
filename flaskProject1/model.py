import pandas as pd
import numpy as np

import tensorflow as tf
import os, cv2

def mapear(cloth):
    if(cloth==0):
        return('Hat')
    elif(cloth==1):
        return('Jacket')
    elif(cloth==2):
        return('Other')
    elif (cloth == 3):
        return ('Shirt')
    elif (cloth == 4):
        return ('Shoe')
    elif (cloth == 5):
        return ('Sweater')
    elif (cloth == 6):
        return ('Trouser')



def send_to_model():
    images_test = os.listdir('./images')
    img_size = 240
    images = []
    for image in images_test:
        path = os.path.join('./images', image)
        if (path!='./images/imageToSave.png'):
            try:
                img_arr = cv2.imread(path)
                resized_arr = cv2.resize(img_arr, (img_size, img_size))  # Reshaping images to preferred size
                images.append([resized_arr, 0])
            except Exception as e:
                print(e)
    x_test = []
    y_test = []

    for feature, label in images:
        x_test.append(feature)
        y_test.append(label)

    x_test = np.array(x_test)
    y_test = np.array(y_test)

    model = tf.keras.models.load_model('./model.h5')


    import matplotlib.pyplot as plt

    y_pred = model.predict(x_test)


    predictions = [np.argmax(prediction) for prediction in y_pred]

    return [mapear(prediction) for prediction in predictions]
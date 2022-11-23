import model3

import cv2
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
import numpy as np
import keras.models
import re
import base64

from flask import request, render_template, Blueprint

Flower = Blueprint("flower", __name__, url_prefix="/flower")

global model, graph

@Flower.route('')
def HomePage():
    return render_template('home.html') # Render home.html

# Route 'classify' accepts GET request
@Flower.route('/classify',methods=['POST','GET'])
def classify_type():
    try:
        sepal_len = request.args.get('slen') # Get parameters for sepal length
        sepal_wid = request.args.get('swid') # Get parameters for sepal width
        petal_len = request.args.get('plen') # Get parameters for petal length
        petal_wid = request.args.get('pwid') # Get parameters for petal width

        # Get the output from the classification model
        variety = model3.classify(sepal_len, sepal_wid, petal_len, petal_wid)

        # Render the output in new HTML page
        return render_template('output.html', variety=variety)
    except:
        return 'Error'

@Flower.route('/mnist')
def index():
    return render_template("index.html")

@Flower.route('/predict/', methods=['GET','POST'])
def predict():
    # get data from drawing canvas and save as image
    parseImage(request.get_data())

    # read parsed image back in 8-bit, black and white mode (L)
    x = cv2.imread('output.png', cv2.IMREAD_GRAYSCALE)
    x = np.invert(x)
    x = cv2.resize(x,(28,28))

    # reshape image data for use in neural network
    x = x.reshape(1,28,28,1)
    with graph.as_default():

        num_classes = 10
        img_rows, img_cols = 28, 28
        input_shape = (img_rows, img_cols, 1)
        model = Sequential()
        model.call = tf.function(model.call)
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))

        #load woeights into new model
        model.load_weights("weights.h5")
        print("Loaded Model from disk")

        #compile and evaluate loaded model
        model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])


        model.call = tf.function(model.call)
        out = model.predict(x)
        print(out)
        print(np.argmax(out, axis=1))
        response = np.array_str(np.argmax(out, axis=1))
        return response

def parseImage(imgData):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('output.png','wb') as output:
        output.write(base64.decodebytes(imgstr))
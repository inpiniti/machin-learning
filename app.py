import model3 # Import the python file containing the ML model
from flask import Flask, request, render_template,jsonify # Import flask libraries
from flask_restx import Resource, Api # Api 구현을 위한 Api 객체 import
from imageio import imsave, imread, imwrite
#from skimage.transform import resize
import numpy as np
import keras.models
import re
import base64
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
sys.path.append(os.path.abspath("./models"))
from load import *

# Initialize the flask class and specify the templates directory
app = Flask(__name__,template_folder="templates")
api = Api(app)  # Flask 객체에 Api 객체 등록

todos = {}
count = 1

global model, graph
model, graph = init()

# Default route set as 'home'
@app.route('/home')
def home():
    return render_template('home.html') # Render home.html

# Route 'classify' accepts GET request
@app.route('/classify',methods=['POST','GET'])
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

@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@api.route('/hello/<string:name>')  # url pattern으로 name 설정
class Hello(Resource):
    def get(self, name):  # 멤버 함수의 파라미터로 name 설정
        return {"message" : "Welcome, %s!" % name}

@api.route('/todos')
class TodoPost(Resource):
    def post(self):
        global count
        global todos

        idx = count
        count += 1
        todos[idx] = request.json.get('data')

        return {
            'todo_id': idx,
            'data': todos[idx]
        }

@api.route('/todos')
class TodoGet(Resource):
    def get(self):

        return todos

@api.route('/todos/<int:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }

    def put(self, todo_id):
        todos[todo_id] = request.json.get('data')
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }

    def delete(self, todo_id):
        del todos[todo_id]
        return {
            "delete" : "success"
        }

@app.route('/mnist')
def index():
    return render_template("index.html")

@app.route('/predict/', methods=['GET','POST'])
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

# Run the Flask server
if(__name__=='__main__'):
    app.run(host='0.0.0.0', port=5000)
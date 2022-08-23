#import model # Import the python file containing the ML model
#from flask import Flask, request, render_template,jsonify # Import flask libraries
#from flask_restx import Resource, Api # Api 구현을 위한 Api 객체 import

# Initialize the flask class and specify the templates directory
#app = Flask(__name__,template_folder="templates")
#api = Api(app)  # Flask 객체에 Api 객체 등록

#todos = {}
#count = 1

# Default route set as 'home'
#@app.route('/home')
#def home():
#    return render_template('home.html') # Render home.html

# Route 'classify' accepts GET request
#@app.route('/classify',methods=['POST','GET'])
#def classify_type():
#    try:
#        sepal_len = request.args.get('slen') # Get parameters for sepal length
#        sepal_wid = request.args.get('swid') # Get parameters for sepal width
#        petal_len = request.args.get('plen') # Get parameters for petal length
#        petal_wid = request.args.get('pwid') # Get parameters for petal width

        # Get the output from the classification model
#        variety = model.classify(sepal_len, sepal_wid, petal_len, petal_wid)

        # Render the output in new HTML page
#        return render_template('output.html', variety=variety)
#    except:
#        return 'Error'

#@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
#class HelloWorld(Resource):
#    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
#        return {"hello": "world!"}

#@api.route('/hello/<string:name>')  # url pattern으로 name 설정
#class Hello(Resource):
#    def get(self, name):  # 멤버 함수의 파라미터로 name 설정
#        return {"message" : "Welcome, %s!" % name}

#@api.route('/todos')
#class TodoPost(Resource):
#    def post(self):
#        global count
#        global todos
#
#        idx = count
#        count += 1
#        todos[idx] = request.json.get('data')
#
#        return {
#            'todo_id': idx,
#            'data': todos[idx]
#        }

#@api.route('/todos')
#class TodoGet(Resource):
#    def get(self):
#
#        return todos

#@api.route('/todos/<int:todo_id>')
#class TodoSimple(Resource):
#    def get(self, todo_id):
#        return {
#            'todo_id': todo_id,
#            'data': todos[todo_id]
#        }
#
#    def put(self, todo_id):
#        todos[todo_id] = request.json.get('data')
#        return {
#            'todo_id': todo_id,
#            'data': todos[todo_id]
#        }
#
#    def delete(self, todo_id):
#        del todos[todo_id]
#        return {
#            "delete" : "success"
#        }

# Run the Flask server
#if(__name__=='__main__'):
#    app.run(host='0.0.0.0', port=5000)
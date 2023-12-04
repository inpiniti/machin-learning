from flask import Flask # Flask 객체 import
from flask_restx import Resource, Api # Api 구현을 위한 Api 객체 import
from flask_cors import CORS # CORS 처리를 위한 모듈 import

from route.naver import Naver
from route.daum import Daum
from route.investing import Investing
from route.krx import Krx
from route.db import Db
from route.dart import Dart
from route.ai import Ai

# 소캣통신을 위해 필요한 모듈
from flask_socketio import SocketIO # pip install flask-socketio
from socket_events import socketio, sendMessage

app = Flask(__name__, template_folder="templates")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

# Flask 객체에 Api 객체 등록
api = Api(app)

api.add_namespace(Naver, '/naver')
api.add_namespace(Daum, '/daum')
api.add_namespace(Investing, '/investing')
api.add_namespace(Krx, '/krx')
api.add_namespace(Db, '/db')
api.add_namespace(Dart, '/dart')
api.add_namespace(Ai, '/ai')

# Socket.IO 서버 생성 및 Flask 앱에 등록
socketio.init_app(app, cors_allowed_origins="*")

# 전역 변수 선언
sectorName = None
sectorCurrentIndex = 0
sectorTotalCount = 0

sectorName = None
sectorCurrentIndex = 0
sectorTotalCount = 0

# 수집중인지?
isCollecting = False

if(__name__=='__main__'):
    app.run(host='0.0.0.0', port=5001)
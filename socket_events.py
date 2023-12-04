from flask_socketio import SocketIO

socketio = SocketIO()

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

def sendMessage(msg):
    print('sendMessage: ' + str(msg))
    socketio.emit('message', msg)
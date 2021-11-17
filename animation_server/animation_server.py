from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

glights = 0

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/door")
def door():
    socketio.emit("door_toggle","toggle")
    return 'OK'


@app.route("/garage_door")
def garage_door():
    socketio.emit("garage_door","toggle")
    return 'OK'

@app.route("/garage_lights")
def garage_lights():
    global glights
    glights ^= 1
    socketio.emit("garage_lights",str(glights))
    return 'OK'

@socketio.on('conn_ack')
def handle_my_custom_event(json):
    print('received json: ' + str(json))



if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    print('Door server running')
    socketio.run(app, host='0.0.0.0', port=5555)

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import requests
app = Flask(__name__)
socketio = SocketIO(app)
ip = '192.168.137.89'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/anim/<thing>')
def door(thing):
    requests.get('http://'+ ip +':5555/'+ thing)
    return 'OK'

@app.route('/door-feed')
def door_feed():
    return render_template('door.html')

@app.route('/lights')
def lights():
    return render_template('lights.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')

@app.route('/others')
def others():
    return render_template('others.html')

@app.route('/intruder')
def intruder():
    socketio.emit('intruder', 'intruder')
    return 'OK'

@socketio.on('connection')
def connection(json):
    print(json)

# if __name__ == '__main__':
def start_server():
    socketio.run(app, host='0.0.0.0', port=5000) # debug only works when run as main thread
    print('Server running...')

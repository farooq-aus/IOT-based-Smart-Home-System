from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import requests
from env import ANIMATION_SERVER_IP
app = Flask(__name__)
socketio = SocketIO(app)
#ip = '192.168.137.89'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/anim/<thing>')
def door(thing):
    requests.get('http://'+ ANIMATION_SERVER_IP +'/'+ thing)
    return 'OK'

@app.route('/door-feed')
def door_feed():
    return render_template('door.html')

@app.route('/motion')
def motion():
    return render_template('motion.html')

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

@app.route('/motiond')
def motiond():
    socketio.emit('motiond', 'motiond')
    return 'OK'

@app.route('/fire/<temp>')
def fire(temp):
    socketio.emit('fire', str(temp))
    return 'OK'

@socketio.on('json')
def handle_json(json):
    print('received json: '+ str(json))
    emit('intruder', 'intruder') 

#if __name__ == '__main__':
def start_server():
    print('Server running...')  
    socketio.run(app, host='0.0.0.0', port=5555) # debug only works when run as main thread
    
    
#start_server()
    

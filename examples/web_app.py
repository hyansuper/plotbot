from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from plotbot import PlotBot
from time import sleep, time
from threading import Thread
from gpiozero import Button

app = Flask(__name__)
socketio = SocketIO(app, async_mode = 'threading')
bot = PlotBot()
user_id = None
timestamp = None
background_thread = None
background_run = True
lines = []

def reset():
    global user_id, lines
    user_id = None
    lines = []
    socketio.emit('reset')
    notify()

button = Button(18, pull_up=True, hold_time=2)
button.when_held = reset

def notify(broadcast=True):
    global user_id
    if broadcast:
        socketio.emit('user', {'id': user_id})
    else:
        emit('user', {'id': user_id})

def background():
    global user_id, timestamp, background_run
    while background_run:
        if user_id and (time() - timestamp > 60):
            user_id = None
            bot.relax()
        sleep(10)
        notify()

@app.route("/")
def index():
    return render_template('drawing.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('./static', path)

@socketio.on('up')
def up():
    global timestamp
    timestamp = time()
    bot.up()
    sleep(.1)
    emit('up', broadcast=True, include_self=False)

@socketio.on('down')
def down(p): 
    global timestamp
    timestamp = time()
    bot.lineto(p)
    sleep(.5)
    bot.down();
    sleep(.1)
    lines.append([p])
    emit('down', p, broadcast=True, include_self=False)

@socketio.on('lineto')
def lineto(p):
    global timestamp
    timestamp = time()
    bot.lineto(p)
    sleep(0.005)
    lines[-1].append(p)
    emit('lineto', p, broadcast=True, include_self=False)

@socketio.on('disconnect')
def disconnect():
    pass    

@socketio.on('occupy')
def occupy(id, occ):
    global user_id
    if occ and not user_id:
        user_id = id
        notify()
    elif not occ and user_id==id:
        user_id = None
        bot.relax()
        notify()

@socketio.on('connect')
def connect():
    emit('lines', lines)    
    notify(False)

import signal
import sys
def signal_handler(sig, frame):
    global background_run
    bot.relax()
    background_run = False
    background_thread.join()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    bot.up()
    sleep(.5)
    bot.relax()
    background_thread = Thread(target = background)
    background_thread.start()
    socketio.run(app, host='0.0.0.0', debug=True)

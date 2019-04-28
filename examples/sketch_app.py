from flask_video_streaming.camera_pi import Camera
from flask import Flask, render_template, Response
from gpiozero import Button
from time import sleep
from threading import Thread
from sketch import to_sketch
from plotbot import PlotBot

bot = PlotBot()
take_picture = False
drawing = False
drawing_thread = None
frame = None

def cam2bot(p):
    """convert camera resolution 720*480 to bot coordinate"""
    return (p[1]/480*55+25, p[0]/480*55-50)

def _stop_drawing():
    global drawing
    bot.relax()
    drawing = False
    Camera().get_frame()
    
def draw():
    global drawing, frame
    lines = to_sketch(frame)
    for line in lines:
        line[0] = cam2bot(line[0])
        bot.lineto(line[0])
        sleep(.3)
        bot.down()
        sleep(.1)
        for p in line[1:]:
            p = cam2bot(p)
            bot.lineto(p)
            sleep(.1)
            if not drawing:
                _stop_drawing()
                return
        bot.up()
        sleep(.1)
    _stop_drawing()            

def held():
    global drawing, drawing_thread
    drawing = True
    drawing_thread = Thread(target=draw)
    drawing_thread.start()
        
def pressed():    
    global take_picture, drawing, drawing_thread
    if drawing:
        drawing = False
        drawing_thread.join()
    else:
        take_picture = True
    
def released():
    global take_picture
    take_picture = False

button = Button(18, pull_up=True, hold_time=3)
button.when_held = held
button.when_pressed = pressed
button.when_released = released

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('camera_sketch.html')

def gen(camera):
    global take_picture, drawing, frame
    while True:
        if take_picture or drawing:
            sleep(1)
            continue
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)

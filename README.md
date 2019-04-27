# plotbot
Python code for [Line-us clone](http://www.buildlog.net/blog/2017/02/a-line-us-clone/).
After reading the post, I redesigned the model with Fusion360. You can download [3D model from Thingiverse]() or the Fusion360 file [here](https://a360.co/2Pvn2hH)

The [Line-us drawing robot](https://www.line-us.com/) is a much finer product than this one.

## Hardware:
* raspberry pi zero w
* Adafruit PCA9685 PWM servo controller
* metal geared 9g servo X3
* 10mm*4mm bearing X3
* button X1

## Dependency: 
    pip install pyyaml adafruit-pca9685 gpiozero flask flask-socketio
    git clone https://github.com/hyansuper/linedraw
    git clone https://github.com/hyansuper/flask_video_streaming

## How to use:
    export PYTHONPATH=$PYTHONPATH:$pwd
    git clone https://github.com/hyansuper/plotbot
    cd plotbot
    change conf.yaml file according to your servo settings
    cd examples
    run 'python web_app.py' or 'python sketch_app.py'
    then visit <pi_zero_ip_address>:5000

## Tips for 3D print:
The stiffness of the arm greatly affects the output, to achieve good result, you'll need good quality bearings, and the 4 links making up the arm should be printed with 100% infill.

# plotbot
Python code for [Line-us clone](http://www.buildlog.net/blog/2017/02/a-line-us-clone/)

Hardware:
* raspberry pi zero w
* Adafruit PCA9685 PWM servo controller
* metal geared 9g servo X3
* 10mm*4mm bearing X3
* button X1

Dependency: 

    pip install pyyaml adafruit-pca9685 gpiozero flask flask-socketio
    git clone https://github.com/hyansuper/linedraw
    git clone https://github.com/hyansuper/flask_video_streaming

How to use:

    git clone https://github.com/hyansuper/plotbot
    cd plotbot
    change conf.yaml file according to your servo settings
    run 'python web_app.py' or 'python sketch_app.py'
    then visit <pi_zero_ip_address>:5000

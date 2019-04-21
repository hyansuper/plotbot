# plotbot
Python code for [Line-us clone](http://www.buildlog.net/blog/2017/02/a-line-us-clone/)

Hardware:
* raspberry pi zero w
* Adafruit PCA9685 PWM servo controller
* metal geared 9g servo X3
* 10mm*4mm bearing X3
* button X1

Dependency: 
* pip install pyyaml
* pip install adafruit-pca9685
* pip install gpiozero
* pip install flask
* pip install flask-socketio

How to play:<br>
&nbsp;&nbsp;cd plotbot<br>
&nbsp;&nbsp;change conf.yaml file according to your servo settings<br>
&nbsp;&nbsp;python webapp.py<br>
&nbsp;&nbsp;then visit <pi_zero_ip_address>:5000<br>

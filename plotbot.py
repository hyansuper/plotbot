import Adafruit_PCA9685
import yaml
import math
import os

class UnreachableCoordinateException(Exception):
    pass

class PlotBot:
    min_x = 20
    ab_diff_min = 20
    ab_diff_max = 160
    link_a = 30
    link_b = 50
    link_pen = 50
    # a,b,c are channels for the 3 servos:
    # a for the lower servo, b for the upper servo, and c for the servo the control pen up/down
    # see in the conf file
    def __init__(self, conf_file = os.path.split(__file__)[0] + '/conf.yaml'):
        with open(conf_file) as f:
            self.conf = yaml.safe_load(f)
            self.pwm = Adafruit_PCA9685.PCA9685()
            self.pwm.set_pwm_freq(60)

    def __del__(self):
        self.relax()

    def save_conf(self, conf_file = os.path.split(__file__)[0] + '/conf.yaml'):
        with open(conf_file, 'w') as f:
            yaml.dump(self.conf, f, default_flow_style = False)

    def up(self):
        self.pwm.set_pwm(self.conf['c']['channel'], 0, self.conf['c']['pwm_up'])

    def down(self):
        self.pwm.set_pwm(self.conf['c']['channel'], 0, self.conf['c']['pwm_down'])

    def _try_angle(self, servo, angle):
        return angle >= self.conf[servo]['angle_min'] and angle <= self.conf[servo]['angle_max']

    def _set_angle(self, servo, angle):
        servo = self.conf[servo]    
        pwm = (servo['pwm_max']-servo['pwm_min'])/(servo['angle_max']-servo['angle_min'])*(angle-servo['angle_min'])+servo['pwm_min']
        self.pwm.set_pwm(servo['channel'], 0, int(pwm))

    def goto(self, x, y):
        if x < self.min_x:
            raise UnreachableCoordinateException(str((x,y))+'x < ' + str(self.min_x))

        # calc angles for a and b:
        try:            
            link_sqr = x**2 + y**2
            link = math.sqrt(link_sqr)
            b = math.acos((link_sqr + self.link_b**2 - self.link_pen**2) / (2*self.link_b*link))
            b += math.atan2(y, x)
            diff = math.acos((self.link_b**2 + self.link_pen**2 - link_sqr) / (2*self.link_pen*self.link_b))
            a = b + diff

            a *= 180/math.pi
            b *= 180/math.pi
            diff *= 180/math.pi

            if diff < self.ab_diff_min or diff > self.ab_diff_max:
                raise UnreachableCoordinateException(str((x,y))+' a-b out of range')
            elif not self._try_angle('a', a):
                raise UnreachableCoordinateException(str((x,y))+'Angle for servo a out of range')
            elif not self._try_angle('b', b):
                raise UnreachableCoordinateException(str((x,y))+'Angle for servo b out of range')
            else:
                self._set_angle('a', a)
                self._set_angle('b', b)

        except ValueError:
            raise UnreachableCoordinateException(str((x,y))+'Calculation error.')

    def relax(self):
        self.pwm.set_all_pwm(0, 0)





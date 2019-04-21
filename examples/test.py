from plotbot import PlotBot
from time import sleep
def drange(start,stop,step):
    r=start
    while True:
        yield r
        r+=step
        if start<stop and r>stop or start>stop and r<stop:
            break

b = PlotBot()
def rect(x1,y1,x2,y2):
    for x in drange(x1,x2,0.1):
        b.goto(x,y1)
        sleep(.0005)
    for y in drange(y1,y2,0.1):
        b.goto(x2,y)
        sleep(.0005)
    for x in drange(x2,x1,-0.1):
        b.goto(x,y2)
        sleep(.0005)
    for y in drange(y2,y1,-0.1):
        b.goto(x1,y)
        sleep(.0005)

rect(25,-50,80,50)

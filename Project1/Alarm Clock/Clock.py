#Joseph Griffith
#9-20-21
#Clock

#imports
from Alarm import *
from tkinter import *
from tkinter import font
from tkinter import ttk
import calendar
import time
import datetime


#time zones
GMT=0
ECT=1
EET=2
ART=3
NET=4
PLT=5
BST=6
VST=7
CTT=8
JST=9
AET=10
SST=11
NST=12
MIT=-11
HST=-10
AST=-9
PST=-8
MST=-7
CST=-6
EST=-5
PRT=-4
CNT=-3
CAT=-1
dls=1
ampm="AM"

def getTimeNow(timeZone,dls=0,military_time=0):
    #calc current time
    seconds = calendar.timegm(time.gmtime())
    current_second = seconds % 60
    minutes = seconds // 60
    current_minute = minutes % 60
    hours = minutes // 60 + timeZone + dls
    current_hour = hours % 24

    ahour, aminute, asecond = set_alarm()
    if current_hour == ahour and current_minute == aminute and current_second == asecond:
        alarm()
    
    #convert to standard time
    if military_time == 0:
        if current_hour > 11:
            ampm = " PM"
        else:
            ampm = " AM"
        current_hour = current_hour % 12
        if current_hour == 0:
            current_hour = 12
    else:
        ampm=""
        ahour, aminute, asecond = set_alarm()
    if current_hour == ahour and current_minute == aminute and current_second == asecond:
        alarm()
    if current_hour < 10:
        current_hour = "0"+str(current_hour)
    if current_minute < 10:
        current_minute = "0"+str(current_minute)
    if current_second < 10:
        current_second = "0"+str(current_second)
    
    current_time = str(current_hour)+":"+str(current_minute)+":"+str(current_second)+ampm

    return current_time
def show_time():
    c_time = getTimeNow(MST,dls)
    txt.set(c_time)
    root.after(1000,show_time)

def quit(*args):
    root.destroy()

def set_alarm():
    ahour = 2
    aminute = 11
    asecond = 30
    return ahour, aminute, asecond

root =Tk()
root.attributes("-fullscreen",False)
root.title("AlarmClock")
root.geometry("800x300")
root.bind("x",quit)
root.bind("a",set_alarm)
root.configure(background = 'black')
root.after(1,show_time)
txt = StringVar()
fnt = font.Font(family="Century Gothic",size = 60, weight = "bold")
lbl = ttk.Label(root,textvariable=txt,foreground="blue",background="black",font=fnt)
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
root.mainloop()

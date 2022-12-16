#!/usr/bin/python3

#Import the tkinter library
from tkinter import *
from tkinter import font
from datetime import datetime, timedelta
from random import randint

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

ptmw = """
2 50 8
1 65 3
1 80 3
1 95 3
1 110 3
1 120 4
"""

xpreg_long = """
2 60 6
2 80 6
"""

xpreg_med = """
2 60 6
2 100 4
"""

curves = {
    "PTMW post cure slow": ptmw,
    "XPreg cure slow": xpreg_long,
    "XPreg cure fast": xpreg_med
    }


class Curve:
    def __init__(self, name, spec):
        self.name = name
        self.spec = spec

    def getxy(self):
        x = [0.0]
        y = [25.0]

        print(self.spec)
        for l in list(self.spec.split('\n')) + [ "-3 25 0" ]:
            if not l:
                continue
            print(l)
            words = l.split(' ')
            curr_x = x[-1]
            curr_y = y[-1]
            temp = float(words[1])
            dpm = float(words[0])
            dwell = float(words[2])
            time = (temp - curr_y) / (dpm * 60)
            if time < 0:
                raise Exception("Negative time: %s" % self.spec)
            x.append(curr_x + time)
            y.append(temp)
            x.append(curr_x + time + dwell)
            y.append(temp)

        return x, y

def plotcurve(curve):
    #curve = Curve("sdf", spec)
    x, y = curve.getxy()
    f.clf()
    a = f.add_subplot(111)
    a.grid()
    a.set_xlabel("Time, hrs")
    a.set_ylabel("Temperature, °C")
    a.plot(x, y)
    canvas.draw()

def plotrun(curve):
    x, y = curve.getxy()
    f_run.clf()
    a = f_run.add_subplot(111)
    a.grid()
    a.set_xlabel("Time, hrs")
    a.set_ylabel("Temperature, °C")
    a.set_title(curve.name)
    a.plot(x, y)
    canvas_run.draw()

def showSelected(event):
    name = lb.get(lb.curselection())
    plotcurve(Curve(name, curves[name]))


ts1 = None
ts2 = None

def labelButtonRelease(event):
    global ts1, ts2
    now = datetime.now()
    if ts1 is not None:
        delta = now - ts1
        print(delta)
        if delta < timedelta(seconds=1):
            print("Goodbye.")
            win.destroy()
    ts1 = ts2
    ts2 = now

def is_armed():
    global b
    return b['bg'] == 'red'

armid = 0

def arm():
    global b, bg, fg, bg, fg, armid
    bg = (b['bg'])
    fg = (b['fg'])
    b['bg'] = 'red'
    b['fg'] = 'white'
    loc_armid = randint(1, 65536)
    armid = loc_armid
    b.config(activebackground='red')
    b.config(activeforeground='white')
    win.after(5000, lambda: disarm(loc_armid))

def disarm(eid):
    global b, bg, fg, armid
    if eid != 0 and armid != eid:
        return
    print("> disarm")
    b.config(bg=bg)
    b.config(fg=fg)
    b.config(activebackground=bg)
    b.config(activeforeground=fg)
    armid = 0


def start():
    if b['text'] == 'Start' and lb.curselection() == ():
        return
    if not is_armed():
        arm()
    else:
        disarm(0)
        name = lb.get(lb.curselection())
        if b['text'] == 'Start':
            top_frame.pack_forget()
            top_frame_run.pack(side=TOP, fill=BOTH, expand=True)
            b.config(text="Stop")
            plotrun(Curve(name, curves[name]))
        elif b['text'] == 'Stop':
            top_frame_run.pack_forget()
            top_frame.pack(side=TOP, fill=BOTH, expand=True)
            b.config(text="Start")
            plotcurve(Curve(name, curves[name]))


#Create an instance of tkinter frame
win = Tk()
#Create a fullscreen window
win.attributes('-fullscreen', True)

top_frame = Frame(win)
#top_frame.grid(row=0, column=0, padx=10, pady=10, sticky=E+W)
top_frame.pack(side=TOP, fill=BOTH, expand=True)

top_frame_run = Frame(win)

bottom_frame = Frame(win)
#bottom_frame.grid(row=1, column=0, pady=10, sticky=E+W)
bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

lframe = Frame(bottom_frame)
lframe.pack(side=BOTTOM, fill=BOTH)

b = Button(lframe,
           text="Start",
           font=('', 60),
           command=start)

# We don't have a mouse, so make active / passive colours the same
b.config(activebackground=b['bg'])
b.config(activeforeground=b['fg'])
b.pack(padx=10, pady=10, side=LEFT)

label= Label(lframe, text= "23°C", font=('', 100, 'bold'))
label.pack(padx=10, pady=(10, 10), side=RIGHT)

label.bind('<ButtonRelease-1>', labelButtonRelease)

lb = Listbox(top_frame,
             font=('', 25),
             width=18,
             height=10)
lb.insert(0, *list(sorted(curves.keys())))
lb.bind('<<ListboxSelect>>', showSelected)

lb.pack(padx=10, pady=10, side=LEFT)

f = Figure(figsize=(6,4), dpi=100)

canvas = FigureCanvasTkAgg(f, top_frame)
#canvas.show()
canvas.get_tk_widget().pack(padx=10, pady=10, side=RIGHT, fill=BOTH)


f_run = Figure(figsize=(18, 4), dpi=100)

canvas_run = FigureCanvasTkAgg(f_run, top_frame_run)
#canvas.show()
canvas_run.get_tk_widget().pack(padx=10, pady=10, side=RIGHT, fill=BOTH)




#label.grid(row=0, column=0, padx=100, pady=100)

win.mainloop()

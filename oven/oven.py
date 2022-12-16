#!/usr/bin/python3

#Import the tkinter library
from tkinter import *
from tkinter import font

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

def showSelected(event):
    #idx= str(event) + '\n' + str(lb.curselection())
    #print(idx)
    name = lb.get(lb.curselection())
    plotcurve(Curve(name, curves[name]))
    #show.configure(text=temp)


#Create an instance of tkinter frame
win = Tk()

#fonts=list(font.families())
#print(fonts)

#Set the geometry
#win.geometry("650x250")

top_frame = Frame(win)
top_frame.grid(row=0, column=0, padx=10, pady=5)

bottom_frame = Frame(win)
bottom_frame.grid(row=1, column=0, padx=10, pady=5)

b = Button(bottom_frame,
           text="exit",
           font=('', 60),
           bg='red',
           fg='white',
           activebackground='red',
           activeforeground='white',
           command=win.destroy)
b.pack(padx=10, pady=10, side=LEFT)

b = Button(bottom_frame,
           text="Replot",
           font=('', 60),
           command=lambda: plotcurve('hello'))
b.pack(padx=10, pady=10, side=LEFT)

label= Label(bottom_frame, text= "23°C", font=('', 100, 'bold'))
label.pack(padx=(10, 10), pady=(10, 10), side=RIGHT)

lb = Listbox(top_frame,
             font=('', 25),
             width=18,
             height=10)
lb.insert(0, *list(sorted(curves.keys())))
lb.bind('<<ListboxSelect>>', showSelected)

lb.pack(padx=(10, 10), pady=(10, 10), side=LEFT)

f = Figure(figsize=(6,4), dpi=100)
a = f.add_subplot(111)
a.grid()
a.set_xlabel("Time, hrs")
a.set_ylabel("Temperature, °C")
a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

canvas = FigureCanvasTkAgg(f, top_frame)
#canvas.show()
canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH)

#label.grid(row=0, column=0, padx=100, pady=100)

#Create a fullscreen window
win.attributes('-fullscreen', True)

win.mainloop()

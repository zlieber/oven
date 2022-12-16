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

curves_config = {
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

class MainUI:
    def __init__(self, curves):
        self.ts1 = None
        self.ts2 = None
        self.armid = 0

        self.curves = curves

        self.root = Tk()
        self.root.attributes('-fullscreen', True)

        self.top_frame = Frame(self.root)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.top_frame_run = Frame(self.root)

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.bottom_right_frame = Frame(self.bottom_frame)
        self.bottom_right_frame.pack(side=BOTTOM, fill=BOTH)

        self.launch_button = Button(self.bottom_right_frame,
                                    text="Start",
                                    font=('', 60),
                                    command=self._launch)

        # We don't have a mouse, so make active / passive colours the same
        self.launch_button.config(activebackground=self.launch_button['bg'])
        self.launch_button.config(activeforeground=self.launch_button['fg'])
        self.launch_button.pack(padx=10, pady=10, side=LEFT)

        self.temp_label = Label(self.bottom_right_frame, text= "23°C", font=('', 100, 'bold'))
        self.temp_label.pack(padx=10, pady=(10, 10), side=RIGHT)

        self.temp_label.bind('<ButtonRelease-1>', self._labelButtonRelease)

        self.curves_listbox = Listbox(self.top_frame,
                     font=('', 25),
                     width=18,
                     height=10)
        self.curves_listbox.insert(0, *list(sorted(self.curves.keys())))
        self.curves_listbox.bind('<<ListboxSelect>>', self._showSelected)

        self.curves_listbox.pack(padx=10, pady=10, side=LEFT)

        self.figure_select = Figure(figsize=(6,4), dpi=100)
        self.canvas_select = FigureCanvasTkAgg(self.figure_select, self.top_frame)

        self.canvas_select.get_tk_widget().pack(padx=10, pady=10, side=RIGHT, fill=BOTH)


        self.figure_run = Figure(figsize=(18, 4), dpi=100)

        self.canvas_run = FigureCanvasTkAgg(self.figure_run, self.top_frame_run)
        self.canvas_run.get_tk_widget().pack(padx=10, pady=10, side=RIGHT, fill=BOTH)

    def _plotcurve(self, curve):
        #curve = Curve("sdf", spec)
        x, y = curve.getxy()
        self.figure_select.clf()
        a = self.figure_select.add_subplot(111)
        a.grid()
        a.set_xlabel("Time, hrs")
        a.set_ylabel("Temperature, °C")
        a.plot(x, y)
        self.canvas_select.draw()

    def _plotrun(self, curve):
        x, y = curve.getxy()
        self.figure_run.clf()
        a = self.figure_run.add_subplot(111)
        a.grid()
        a.set_xlabel("Time, hrs")
        a.set_ylabel("Temperature, °C")
        a.set_title(curve.name)
        a.plot(x, y)
        self.canvas_run.draw()

    def _showSelected(self, event):
        name = self.curves_listbox.get(self.curves_listbox.curselection())
        self._plotcurve(Curve(name, self.curves[name]))

    def _labelButtonRelease(self, event):
        now = datetime.now()
        if self.ts1 is not None:
            delta = now - self.ts1
            print(delta)
            if delta < timedelta(seconds=1):
                print("Goodbye.")
                self.root.destroy()
        self.ts1 = self.ts2
        self.ts2 = now

    def _is_armed(self):
        return self.launch_button['bg'] == 'red'

    def _arm(self):
        self.bg = (self.launch_button['bg'])
        self.fg = (self.launch_button['fg'])
        self.launch_button['bg'] = 'red'
        self.launch_button['fg'] = 'white'
        loc_armid = randint(1, 65536)
        self.armid = loc_armid
        self.launch_button.config(activebackground='red')
        self.launch_button.config(activeforeground='white')
        self.root.after(5000, lambda: self._disarm(loc_armid))

    def _disarm(self, eid):
        if eid != 0 and self.armid != eid:
            return
        print("> disarm")
        self.launch_button.config(bg=self.bg)
        self.launch_button.config(fg=self.fg)
        self.launch_button.config(activebackground=self.bg)
        self.launch_button.config(activeforeground=self.fg)
        self.armid = 0

    def _launch(self):
        if self.launch_button['text'] == 'Start' and self.curves_listbox.curselection() == ():
            return
        if not self._is_armed():
            self._arm()
        else:
            self._disarm(0)
            name = self.curves_listbox.get(self.curves_listbox.curselection())
            if self.launch_button['text'] == 'Start':
                self.top_frame.pack_forget()
                self.top_frame_run.pack(side=TOP, fill=BOTH, expand=True)
                self.launch_button.config(text="Stop")
                self._plotrun(Curve(name, self.curves[name]))
            elif self.launch_button['text'] == 'Stop':
                self.top_frame_run.pack_forget()
                self.top_frame.pack(side=TOP, fill=BOTH, expand=True)
                self.launch_button.config(text="Start")
                self._plotcurve(Curve(name, self.curves[name]))

    def run(self):
        self.root.mainloop()

ui = MainUI(curves_config)
ui.run()

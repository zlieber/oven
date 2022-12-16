
from tkinter import *
from tkinter import font
from datetime import datetime, timedelta
from random import randint

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from curve import Curve

class MainUI:
    def __init__(self, curves, oven_controller, temp_monitor):
        self.ts1 = None
        self.ts2 = None
        self.armid = 0

        self.oven_controller = oven_controller
        self.temp_monitor = temp_monitor
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
        self.templog_x = None
        self.templog_y = None
        self.root.after(1000, self._temp_update)

    def _temp_update(self):
        temp = self.temp_monitor.get_temperature()
        self.temp_label.config(text = "%.01f°C" % temp)
        self.root.after(1000, self._temp_update)
        if self.templog_x is not None:
            heat_operation = self.oven_controller.on_temp_data(temp)
            if heat_operation == "ON":
                self.temp_label.config(fg = "red")
            elif heat_operation == "OFF":
                self.temp_label.config(fg = "black")
            hrs = self.run_curve.hours_now(self.start_time)
            self.templog_x.append(hrs)
            self.templog_y.append(temp)
            self._plotrun(self.run_curve)

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
        if len(self.templog_x) == 0:
            max_x = 0.5
        else:
            max_x = max(self.templog_x[-1], 0.5)
        a.set_xlim([0, max_x])
        a.plot(x, y)
        if self.templog_x is not None:
            a.plot(self.templog_x, self.templog_y)
        self.canvas_run.draw()

    def _showSelected(self, event):
        name = self.curves_listbox.get(self.curves_listbox.curselection())
        self._plotcurve(Curve(name, self.curves[name]))

    def _labelButtonRelease(self, event):
        now = datetime.now()
        if self.ts1 is not None:
            delta = now - self.ts1
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
                self.templog_x = []
                self.templog_y = []
                self.start_time = datetime.now()
                self.launch_button.config(text="Stop")
                self.run_curve = Curve(name, self.curves[name])
                self._plotrun(self.run_curve)
                self.oven_controller.start(self.run_curve)
            elif self.launch_button['text'] == 'Stop':
                self.templog_x = None
                self.templog_y = None
                self.top_frame_run.pack_forget()
                self.top_frame.pack(side=TOP, fill=BOTH, expand=True)
                self.launch_button.config(text="Start")
                self._plotcurve(Curve(name, self.curves[name]))
                self.oven_controller.stop()
                self.temp_label.config(fg = "black")

    def run(self):
        self.root.mainloop()


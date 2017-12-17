import datetime
import time
import tkinter as tk
from tkinter import ttk


class TimeOut(tk.Frame):
    def __init__(self, master=None, days=0, seconds=0):
        tk.Frame.__init__(self, master)
        self.master = master
        self.on_off_status = 0
        self.days, self.seconds = days, seconds
        self.p_flag = False

        self.end_value = '00:00:00'
        self.gui()

    def gui(self):

        style = ttk.Style()
        style.configure('Blue.TEntry', foreground='blue')
        style.configure('Red.TEntry', foreground='red')

        self.txtvar = tk.StringVar()
        self.txtvar.set(self.end_value)
        self.entry = ttk.Entry(self, textvariable=self.txtvar, justify=tk.CENTER)
        self.entry.grid(row=0, column=0)

        self.butvar=tk.IntVar()
        self.but = ttk.Button(self, text='Start/ Stop', command=self.but_press, textvariable=self.butvar)
        self.but.grid(row=1, column=0)

    def time_out(self, days=0, seconds=0):

        def update_clock():
            time_left = future - datetime.datetime.now()
            if time_left.total_seconds() > 0:
                # Change Color
                if time_left.total_seconds() > 3:
                    self.entry['style'] = 'Blue.TEntry'
                elif time_left.total_seconds() <= 3:
                    self.entry['style'] = 'Red.TEntry'
                # Split microseconds
                time_str = str(time_left).split('.')[0]

                self.entry['width'] = max(len(time_str), 15)
                self.txtvar.set(time_str)
                self.on_off_status = 1

                self.a = self.after(500, update_clock)

            else:
                self.txtvar.set(self.end_value)
                self.after_cancel(self.a)
                self.on_off_status = 0

        now = datetime.datetime.now()
        future = now + datetime.timedelta(days, seconds)
        update_clock()

    def but_press(self):
        if self.p_flag:
            #print("stop", self.p_flag)
            self.after_cancel(self.a)
        elif self.p_flag == False:
            #print("start", self.p_flag)
            #self.but_press['fg']='green'
            a = datetime.datetime.strptime(self.txtvar.get(), '%H:%M:%S').timetuple()

            self.time_out(days=0, seconds=datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).total_seconds())

        self.p_flag = not self.p_flag

    def long_press(self):
        print()
    def status(self):
        return self.on_off_status


root = tk.Tk()
a = TimeOut(root, days=0, seconds=15)
a.grid()
root.mainloop()

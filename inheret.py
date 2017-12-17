from tkinter import ttk
import tkinter as tk
import datetime


class Core(ttk.Frame):
    def __init__(self, master, text='Not_given'):
        ttk.Frame.__init__(self, master)
        self.style = ttk.Style()
        self.style.configure('Guy.TLabelframe', background='yellow')
        self.frame1 = ttk.Labelframe(self, text="Hi, I'm a labelFrame", style='Guy.TLabelframe', border=5,
                                     relief=tk.SUNKEN)
        self.frame1.grid(row=0, column=1)

        self.label_var = tk.StringVar()
        self.label_var.set(text)

        self.build_gui()

    def build_gui(self):
        ttk.Label(self.frame1, textvariable=self.label_var).grid(row=0, column=0)


class ChildOf(Core):
    def __init__(self, master, text2=''):
        Core.__init__(self, master, text="This text is in Core Class")
        print(text2)
        self.checkbutton_var = tk.IntVar()
        self.button_var = tk.IntVar()

        self.run()

    def run(self):
        ttk.Label(self, text="This text is created in Child Class").grid(row=1, column=0)

        self.check = ttk.Checkbutton(self, text="PressIT to find out", variable=self.checkbutton_var)
        self.check.grid(row=2, column=1)

        self.but = ttk.Button(self, text="Press Me Too!", command=lambda: self.button_cb(event=None))
        self.but.grid(row=3, column=1)

        self.check.bind('<Button-1>', self.button_cb)

    def button_cb(self, event):
        print("Time is:{}".format(datetime.datetime.now()))


root = tk.Tk()
# Core(root,'Good morning Carmiel').grid()
tk.Label(root, text="This text is created in Root").grid(row=0, column=0)
root.config(background='green')
ChildOf(root, text2='Help me').grid(row=1, column=1)

root.mainloop()

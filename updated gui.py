# import tkinter as tk
# from tkinter import ttk
# import datetime
# import os
#
# counter = 0
#
#
# def counter_label(label):
#     counter = 0
#
#     def count():
#         # now=datetime.datetime.now()
#         # global counter
#         # counter += 1
#         label.config(text=str(datetime.datetime.now().replace(microsecond=0)))
#         label.after(1000, count)
#
#     count()
#
#
# def ping(address):
#     # return not
#     print(os.system('ping %s -n 2 >NUL' % (address)))
#
#
# import shlex
# import subprocess
#
# # Tokenize the shell command
# # cmd will contain  ["ping","-c1","google.com"]
# cmd = shlex.split("ping -c1 google.com")
# try:
#     output = subprocess.check_output(cmd)
# except subprocess.CalledProcessError:
#     # Will print the command failed with its exit status
#     print("The IP {0} is NotReacahble".format(cmd[-1]))
# else:
#     print("The IP {0} is Reachable".format(cmd[-1]))
#
# root = tk.Tk()
# ping('google.com')
# root.title("Clock&Date")
# label = ttk.Label(root)
# label.pack()
# counter_label(label)
# button = ttk.Button(root, text='Stop', width=25, command=root.destroy)
# button.pack()
#
# root.mainloop()

import tkinter as tk
from tkinter import ttk
from time import sleep


class NewEntry(ttk.Frame):
    """ This creates an Entry and a press button widgets. Entring value to Entry and pressing the button print it out"""

    def __init__(self, master=None, def_val='Enter Value', kw_ent=None, kw_but=None):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.def_val = def_val
        if kw_ent is None: kw_ent = {}
        if kw_but is None: kw_but = {}

        self.ent_var = tk.StringVar()
        self.ent = ttk.Entry(self, textvariable=self.ent_var, **kw_ent)
        self.ent.grid(row=0, column=0)

        self.button = ttk.Button(self, text='Button', command=self.but_callback, **kw_but)
        self.button.grid(row=0, column=1)
        self.ent.bind('<FocusIn>', self.clear_ent)
        self.ent.bind('<Return>', self.key_callback)

        self.init_vals(self.def_val)

    def init_vals(self, def_val=None):
        if def_val is None:
            self.ent_var.set(self.def_val)
        else:
            self.ent_var.set(def_val)

        self.ent['foreground'] = 'red'

    def clear_ent(self, event):
        self.ent_var.set('')
        self.ent['foreground'] = '#4c4c4c'

    def restore_ent(self, event):
        self.init_vals()

    def key_callback(self, event):
        self.but_callback()
        self.button.focus()

    def but_callback(self):
        print(self.ent_var.get())
        sleep(0.5)
        self.init_vals("Again...")


root = tk.Tk()
a = NewEntry(root, kw_ent={"width": 13}, kw_but={"width": 8})
a.grid()
root.mainloop()

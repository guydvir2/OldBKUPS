import tkinter
from tkinter import ttk
import subprocess


class XWin:
    def __init__(self, master, exec_command):
        self.bg = 'light slate gray'
        self.master = master
        self.toplevel1 = tkinter.Toplevel(self.master, bg=self.bg)
        self.make_gui(exec_command)
        style = ttk.Style()
        style.configure('.', background=self.bg)
        style.configure('bold.TLabel', foreground='white', font='Times 12 ')
        style.configure('header.TLabel', foreground='white', font='Times 14 underline')

    def make_gui(self, exec_command):
        ypad = 5

        def key_cb(event):
            self.exec_command()

        self.toplevel1.title("Enter Passsword")
        frame2 = ttk.Frame(self.toplevel1)
        frame2.grid(row=0, column=0, pady=ypad)

        header = ttk.Label(frame2, text="Confirm running Shell command", style='header.TLabel')
        header.grid()

        frame1 = ttk.Frame(self.toplevel1)
        frame1.grid(row=1, column=0, padx=10, pady=ypad)

        label1 = ttk.Label(frame1, text="program to execute: ")
        label1.grid(row=0, column=0, pady=ypad)

        label2 = ttk.Label(frame1, text=exec_command, style='bold.TLabel')  # , relief="ridge", padding=5)
        label2.grid(row=0, column=1, sticky=tkinter.W)

        label3 = ttk.Label(frame1, text="sudo's password: ")
        label3.grid(row=1, column=0, sticky=tkinter.E, pady=ypad)

        self.ent = ttk.Entry(frame1, width=30, show="@")
        self.ent.grid(row=1, column=1)
        self.ent.bind("<Return>", key_cb)

        but_ok = ttk.Button(frame1, text="Continue", command=self.exec_command)
        but_ok.grid(row=2, column=1, sticky=tkinter.E, pady=ypad)

        but_cancel = ttk.Button(frame1, text="Cancel", command=self.toplevel1.destroy)
        but_cancel.grid(row=2, column=1, sticky=tkinter.W)



    def exec_command(self):
        print(self.ent.get())
        # exec_com = subprocess.Popen('dirl', shell=True, stdout=subprocess.PIPE)
        # print(exec_com.returncode)


def pop_window():
    XWin(root, 'pigpiod')


root = tkinter.Tk()
# button = tkinter.Button(root, text="ActiveMe", command=pop_window)
# button.grid()
XWin(root, 'pigpiod')
root.mainloop()


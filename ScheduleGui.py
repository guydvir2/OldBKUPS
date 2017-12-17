from tkinter import *
from tkinter import ttk


class SchedGui:
    def __init__(self, master=None):
        bg = 'SteelBlue3'
        self.master = master
        self.style = ttk.Style()
        self.style.configure('TLabelFrame', background=bg)
        self.frame = ttk.LabelFrame(self.master, text="MainFrame")
        self.frame.grid(row=0, column=0, padx=30)
        self.gui_line(3)

    def gui_line(self, m):
        for r in range(m):
            def ver_sep(x):
                sp1 = ttk.Separator(self.frame, orient=VERTICAL)
                sp1.grid(row=r, column=x, sticky=N + S + W, padx=5)

            lab1var = StringVar()
            label1 = ttk.Label(self.frame, width=5, background="white", relief=GROOVE, anchor=CENTER,
                               state=DISABLED, textvariable=lab1var)
            label1.grid(row=r, column=0)
            ver_sep(1)

            chkvar = IntVar()
            chktxt = StringVar()
            chktxt.set('Select')

            def chg_chk1():
                if chkvar.get() == 1:
                    chktxt.set("TaskOn ")
                if chkvar.get() == 0:
                    chktxt.set("TaskOff")

            chk1 = ttk.Checkbutton(self.frame, variable=chkvar, textvariable=chktxt, command=chg_chk1, width=8)
            chk1.grid(row=r, column=2)
            ver_sep(3)

            days = []
            dow = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
            for i in range(len(dow)):
                daychk = IntVar()
                day = ttk.Checkbutton(self.frame, variable=daychk, text=dow[i])
                day.grid(row=r, column=4 + i)
                days.append(day)
            ver_sep(11)

            ent1var = StringVar()
            ent1 = ttk.Entry(self.frame, width=8, justify=CENTER, textvariable=ent1var)
            ent1.grid(row=r, column=12)

            ent2var = StringVar()
            ent2 = ttk.Entry(self.frame, width=8, justify=CENTER, textvariable=ent2var)
            ent2.grid(row=r, column=13)
            ver_sep(14)

            ent3var = StringVar()
            ent3 = ttk.Entry(self.frame, width=12, justify=CENTER, textvariable=ent3var, state=DISABLED)
            ent3.grid(row=r, column=15)
            # spHor = ttk.Separator(self.frame,orient=HORIZONTAL)
            # spHor.grid(row=r+1, column=0, sticky=E+W, columnspan=16, pady=5)


root = Tk()
root.config(bg='green')
A = SchedGui(root)

mainloop()

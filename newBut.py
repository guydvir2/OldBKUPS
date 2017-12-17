from tkinter import *


class DoubleButton(Checkbutton):
    def __init__(self, master):
        self.b_var = IntVar()
        Checkbutton.__init__(self,master, bg="yellow", variable=self.b_var)
        self.config(text="Test", width=5, command=self.do)

    def do(self):
        print(self.b_var, self.b_var.get())


root = Tk()

a1 = DoubleButton(root)
a1.grid(row=0, column=0)

a2 = DoubleButton(root)
a2.grid(row=0, column=1)

root.mainloop()

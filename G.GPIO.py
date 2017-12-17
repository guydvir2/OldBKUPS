from tkinter import ttk
from tkinter import *

root = Tk()

root.title("Test Gui to learn ttk")
root.geometry("500x200")

s = ttk.Style()
bg = 'SteelBlue3'
s.configure('.', background=bg)
frame1 = ttk.Frame(root, height=200, width=250)
frame1.grid_propagate(0)
frame1.grid(row=0, column=0)

s.configure('TButton', foreground="black")
#s.configure('TLabel', background=bg)
#layout = s.layout('TButton')
#print(layout)
#print(s.element_options('Button.focus'))

but1 = ttk.Button(frame1, text="ttk Button")
but1.grid(row=1, column=0, columnspan=1, pady=5)
sp = ttk.Separator(frame1, orient=HORIZONTAL)
sp.grid(row=1, column=0, sticky= W+E+N,columnspan=2)
chkbut1 = ttk.Checkbutton(frame1, text="Check")
chkbut1.grid()
label1 = ttk.Label(frame1, text="|ttk definitions|")
label1.grid(row=0, column=0, columnspan=1)
ent1 = ttk.Entry(frame1, width=15)
ent1.grid(row=2, column=1,sticky=E)
ent2 = ttk.Entry(frame1)
ent2.grid(row=2, column=2)
cb=ttk.Combobox(frame1,values=["guy",'Dvir'],width=15,state="readonly")
cb.current([0])
cb.grid()
label2 = ttk.Label(frame1, text="|col 2 ACBDEFGHIJKLMNOP|")
label2.grid(row=0, column=1)
# d = s.element_options('Button.highlight')
# print(d)


frame2 = Frame(root, bg="lightgreen", height=200, width=150)
frame2.grid_propagate(0)
frame2.grid(row=0, column=1)
label2 = Label(frame2, text="Tkinter definitions")
label2.grid(row=0, column=0, columnspan=2)
but2 = Button(frame2, text="Button", activebackground="green", activeforeground="yellow", anchor=W, height=2, width=10,
              highlightbackground="lightgreen", highlightcolor="brown", relief=RAISED, overrelief=GROOVE)
but2.grid(row=1, column=0, sticky=E + W)
chkbut2 = Checkbutton(frame2, text="CheckButton", background="blue", fg="red", activebackground="cyan", height=2,
                      indicatoron=1)
chkbut2.grid(row=2, column=0)

rb = Radiobutton(frame2)
rb.grid(row=3, column=0)

mainloop()

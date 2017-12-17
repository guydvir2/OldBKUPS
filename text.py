from tkinter import *
from guizero import *
import time

root = Tk()
text = Text(root)
text.grid(row=0, column=0)

Ss = Scrollbar(root)
Ss.grid(row=0, column=1, sticky=N + S + W + E)
Ss.config(command=text.yview)
text.config(yscrollcommand=Ss.set)
b = "\n"
for t in range(100):
    text.insert(END, str(t)+b)
    #time.sleep(0.5)

led = LED(17)

root.mainloop()

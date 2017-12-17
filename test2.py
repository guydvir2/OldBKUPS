# import tkinter as tk
# from tkinter import filedialog
#
# root = tk.Tk()
# root.withdraw()
#
# file_path = filedialog.askdirectory(title='Select folder for Log file')
# print(file_path)
# #root.mainloop()



import tkinter as tk
from tkinter import ttk


class TxtSwitch(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        ttk.Frame.__init__(self, master)
        self.frame = ttk.Frame(self)
        self.frame.grid()
        ttk.Label(self.frame, text="On ", foreground='green').grid(row=0, column=0)
        ttk.Label(self.frame, text=" Off", foreground='red').grid(row=0, column=2)
        self.txtvar = tk.StringVar()
        self.sw_state_label = ttk.Label(self.frame, textvariable=self.txtvar)
        self.sw_state_label.bind('<Button-1>', self.switch_to)
        self.sw_state_label.grid(row=0, column=1)
        self.state = -1
        self.switch_to(event='', state=1)

    def switch_to(self, event, state=None):
        if state == 0 or self.state == 1:
            self.txtvar.set('__##')
            self.sw_state_label['foreground'] = 'red'
            self.state = 0
        elif state == 1 or self.state == 0:
            self.txtvar.set('##__')
            self.sw_state_label['foreground'] = 'green'
            self.state = 1
        print('Switched', ['Off','On'][self.state])

    def get_state(self):
        return self.state


root = tk.Tk()
a = TxtSwitch(root)
a.grid()
print(a.get_state())
a.switch_to(event='', state=0)
print(a.get_state())
root.mainloop()

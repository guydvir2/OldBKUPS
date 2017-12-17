import tkinter
from time import sleep


class ThreeWayBut(tkinter.Frame):
    def __init__(self, master, nickname='', text_up='UP', text_down='DOWN', width=15, height=3, hw_in=[], hw_out=[],
                 ip_in='', ip_out=''):
        tkinter.Frame.__init__(self, master)
        self.nick = nickname
        self.master = master
        self.but_stat = []
        self.build_buttons(text_up, text_down, width, height)

    def build_buttons(self, text_up, text_down, width, height):

        but1_var = tkinter.IntVar()
        but1 = tkinter.Checkbutton(self, text=text_up, width=width, height=height, indicatoron=0, variable=but1_var,
                                   command=self.com_up)
        but1.grid(row=0, column=0, pady=5)

        but2_var = tkinter.IntVar()
        but2 = tkinter.Checkbutton(self, text=text_down, width=width, height=height, indicatoron=0, variable=but2_var,
                                   command=self.com_down)
        but2.grid(row=1, column=0)

        label = tkinter.Label(self, text=self.nick)
        label.grid(row=2, column=0)

        self.but_stat = [but1_var, but2_var]

    def com_up(self):
        if self.but_stat[0].get() == 1:
            if self.but_stat[1].get() == 1:
                self.but_stat[1].set(0)
                self.status(0, self.but_stat[1].get())
                sleep(1)
                self.status(self.but_stat[0].get(), self.but_stat[1].get())
            elif self.but_stat[1].get() == 0:
                self.status(self.but_stat[0].get(), self.but_stat[1].get())
        elif self.but_stat[0].get() == 0:
            self.status(self.but_stat[0].get(), self.but_stat[1].get())

    def com_down(self):
        if self.but_stat[1].get() == 1:
            if self.but_stat[0].get() == 1:
                self.but_stat[0].set(0)
                self.status(self.but_stat[0].get(), 0)
                sleep(1)
                self.status(self.but_stat[0].get(), self.but_stat[1].get())
            elif self.but_stat[0].get() == 0:
                self.status(self.but_stat[0].get(), self.but_stat[1].get())
        elif self.but_stat[1].get() == 0:
            self.status(self.but_stat[0].get(), self.but_stat[1].get())

    def status(self, up_stat, down_stat):
        output1 = [self.nick, up_stat, down_stat]
        print(output1)
        return output1


class MainApp:
    def __init__(self, master, amount):
        self.build_buttons(root, amount)

    def build_buttons(self, frame, amount):
        buttons_vector = []
        nicks = ['חלון', 'מטבח', 'גינה']
        for i in range(amount):
            buttons_vector.append('but_' + str(i))
            try:
                nicks[i]
            except IndexError:
                nicks.append('Button#%d'%i)
            buttons_vector[i] = ThreeWayBut(frame, nicks[i])
            buttons_vector[i].grid(row=0, column=i, padx=10)

    def get_status(self):
        pass


root = tkinter.Tk()
App = MainApp(root, 8)

root.mainloop()

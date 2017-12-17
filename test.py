# import tkinter as tk
#
# class MainScreen(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         self.pack()
#         self.parent = parent
#
#         self.push_count = 0
#
#         self.button = tk.Button(
#             self,
#             text = 'Character Window',
#             command = self.new_window)
#         self.button.pack()
#
#         self.push_counter = tk.Button(
#             self,
#             text = 'You need to click me',
#             command = self.push_me)
#         self.push_counter.pack()
#
#     def new_window(self):
#         self.button['state'] = tk.DISABLED
#         self.newWindow = tk.Toplevel(self)
#         CharWindow(self) #pass the entire self class
#
#     def push_me(self):
#         self.push_count += 1
#         self.push_counter['text'] = "you pushed me %d times"%self.push_count
#
# class CharWindow(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent.newWindow)
#         self.pack()
#         self.parent = parent
#
#         self.push_count = 0
#
#         self.quitButton = tk.Button(
#             self,
#             text = 'Quit',
#             command = self.close_windows)
#         self.quitButton.pack()
#
#         self.push_counter = tk.Button(
#             self,
#             text = 'You need to click me',
#             command = self.push_me)
#         self.push_counter.pack()
#
#     def close_windows(self):
#         self.parent.button['state'] = tk.NORMAL #so now you have the MainScreen instance available as self.parent
#         self.parent.newWindow.destroy()
#
#     def push_me(self):
#         self.push_count += 1
#         self.push_counter['text'] = "you pushed me %d times"%self.push_count
#
# def main():
#     root = tk.Tk()
#     app = MainScreen(root)
#     root.mainloop()
#
# if __name__ == '__main__':
#     main()

from tkinter import *

m1 = PanedWindow()
m1.pack(fill=BOTH, expand=1)

left = Label(m1, text="left pane")
m1.add(left)

m2 = PanedWindow(m1, orient=VERTICAL)
m1.add(m2)

top = Label(m2, text="top pane")
m2.add(top)

bottom = Label(m2, text="bottom pane")
m2.add(bottom)

mainloop()
# import Schedule
# import tkinter
#
#
# def recurring_run():
#     sched1.task_time_status()
#     sched2.task_time_status()
#     var1.set('Sched1:'+str(sched1.get_status()[0][0])+", " +str(sched1.get_status()[0][1]))
#     var2.set('Sched2:'+str(sched2.get_status()[0][0])+", " +str(sched2.get_status()[0][1]))
#     root.after(1000, recurring_run)
#
#
# root = tkinter.Tk()
# sched1 = [[1, "14:25:30", "14:26:00"]]
# sched1 = Schedule.ScheduledEvents(sched1)
#
# sched2 = [[7, "08:40:00", "17:50:10"]]
# sched2 = Schedule.ScheduledEvents(sched2)
#
# var1 = tkinter.StringVar()
# lab1 = tkinter.Label(root, textvariable=var1)
# lab1.pack()
#
# var2 = tkinter.StringVar()
# lab2 = tkinter.Label(root, textvariable=var2)
# lab2.pack()
#
# recurring_run()
#
# root.mainloop()
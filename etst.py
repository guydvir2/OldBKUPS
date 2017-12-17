# from tkinter import *
# from tkinter import ttk
#

# def change():
#      print(entry.configure())
#
#
# root = Tk()
# frame1 = Frame(root)
# frame1.grid()
# entry = Entry(frame1, bg='lightblue', state=DISABLED)
# entry.grid()
# button = Button(frame1,text="HELP ME!",command=change)
# button.grid()
# root.mainloop()
#

# root = Tk()
# w = '200'
# h = '80'
# root.geometry('{}x{}'.format(w, h))
# root.configure(bg='lightgreen')    ###To diff between root & Frame
# root.resizable(False, False)
#
# txt = StringVar()
# txt.set("This is an error message")
#
# testframe = ttk.Frame(root)
# testframe.grid(row=0, column=1)
#
# label1 = ttk.Label(testframe, textvariable=txt)
# label1.grid(row=0, column=0, pady=10)
#
# ok_button = ttk.Button(testframe, text="OK", command=root.destroy)
# ok_button.grid()
#
# testframe.update()
#
# xbias = int(w) / 2 - testframe.winfo_width() / 2
# ybias = int(h) / 2- testframe.winfo_height() / 2
# testframe.grid(row=0, column=1, pady=ybias, padx=xbias)
#
# root.mainloop()
#
#
# import tkinter as tk
# from tkinter import ttk
#
#
# class CanvasWidgets(ttk.Frame):
#     def __init__(self, master,  width=100, height=100):
#         ttk.Frame.__init__(self, master)
#         self.width, self.height = width, height
#         self.frame = ttk.Frame(self)
#
#         self.build_gui()
#
#     def build_gui(self):
#         self.canvas = tk.Canvas(self, width=400, bg='light green')
#         self.frame.lift()
#         self.frame.bind("<Configure>", self.onFrameConfigure)
#         self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
#         self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
#         self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
#         self.vsb.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W)
#         self.hsb.grid(row=1, column=0, sticky=tk.W + tk.N + tk.E, columnspan=2)
#         self.canvas.create_window((4, 4), window=self.frame, anchor="nw")
#
#         self.canvas.grid(row=0, column=0)
#
#     def onFrameConfigure(self, event):
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
#
# root = tk.Tk()
# frame = ttk.Frame(root)
#
# a = CanvasWidgets(root)
# a.grid()
# rows, cols = 20, 20
# for row in range(rows):
#     for col in range(cols):
#         ttk.Label(a.frame, text=[row, col], relief=tk.SUNKEN, width=5).grid(row=row, column=col, sticky=tk.E)
#
#
# root.mainloop()


#
# canvas =
# sub_frame = ttk.Frame(canvas)
#
# rows = 50
# cols = 10
# for row in range(rows):
#     for col in range(cols):
#         ttk.Label(sub_frame, text=[row, col], relief=tk.SUNKEN, width=5).grid(row=row, column=col, sticky=tk.E)
# sub_frame.bind("<Configure>", onFrameConfigure)
# vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
# hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
# canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
# vsb.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W)
# hsb.grid(row=1, column=0, sticky=tk.W + tk.N + tk.E)
# canvas.create_window((4, 4), window=sub_frame, anchor="nw")
# # a= tk.Label(sub_frame, text="GUY")
# # a.grid()
# canvas.grid(row=0, column=0)
# root.mainloop()



from tkinter import *

root = Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

w = Canvas(root, width=200, height=100)
w.grid(sticky=N+S+E+W)

w.create_line(0, 0, 200, 100)
w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

w.create_rectangle(50, 25, 150, 75, fill="blue")

root.mainloop()
# import tkinter as tk
# from tkinter import ttk
#
#
# class MainSheet(tk.Frame):
#     def __init__(self, master):
#         tk.Frame.__init__(self, master)
#         self.var_bundle = []
#         self.var_bundle = []
#         self.frame1 = tk.Frame(self)
#         self.frame1.pack()
#         self.create_entries()
#
#     def create_entries(self):
#         for r in range(2):
#             for c in range(3):
#                 a = tk.IntVar()
#                 a.set([r,c])
#                 b = ttk.Entry(self.frame1, textvariable=a)
#                 b.pack(padx=5, pady=5, side=tk.TOP, fill=tk.BOTH, expand=500)
#
#                 self.var_bundle.append(a)
#             b.pack()
#         print(self.var_bundle)
#
#     def create_butt(self):
#
#         print(self.var_bundle)
#
#
# root = tk.Tk()
# a = MainSheet(root)
# a.pack()
# root.mainloop()
#

def xtrct_nums(lista):
    new_list = []
    def xtrct_str(listb):
        new_lst = []
        temp = ''

        for i in range(len(listb)):
            try:
                int(listb[i])  # try in int
                temp = temp + listb[i]  # use is as char !
            except ValueError:
                if not temp == '':
                    new_lst.append(int(temp))
                    temp = ''
            # for last number in str
            if i == len(listb) - 1 and not temp == '':
                new_lst.append(int(temp))

        return new_lst

    if type(lista) is str:
        new_list = xtrct_str(lista)

    elif type(lista) is list:
        for item in lista:
            if type(item) is int:
                new_list.append(item)
            elif type(item).__name__ == 'str':
                z = xtrct_str(item)
                if not z == []: new_list.append(xtrct_str(item)[0])

    return new_list

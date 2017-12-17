import csv
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class ReadFile:
    """This class reads CSV w/out header line, and returen it as a list"""

    def __init__(self, fname='', path='', **kwargs):
        if fname == '' and path == '':
            gui = tk.Tk()
            gui.withdraw()
            self.filename = askopenfilename(title='Select CSV file', filetypes=[('CommaSeperatedFile', '*.csv')])
            gui.destroy()

        else:
            if path != '':
                self.filename = path + '/' + fname
            else:
                self.filename = fname

        self.file_content = []
        self.read_file(kwargs)

    def read_file(self, kwargs):
        with open(self.filename, newline='', **kwargs) as csvfile:
            file_obj = csv.reader(csvfile)
            for i in file_obj:
                self.file_content.append(i)

        print("file %s read successfully, containing %d lines" % (self.filename, len(self.file_content)))

    def out_in_gui(self):
        print("send data to CSVGui")
        CSVGui(data=self.file_content, filename=self.filename)

    def file_contents(self):
        return self.file_content


class CSVGui(ttk.Frame):
    def __init__(self, data=[], filename='', rows=20, cols=10):
        # Build Frame
        self.gui = tk.Tk()
        self.gui.resizable(False, False)

        self.gui.title("Simple CSV Viewer/Editor")

        ttk.Frame.__init__(self, self.gui)
        self.grid()

        self.toolbar_frame = ttk.Frame(self, border=4)
        self.toolbar_frame.grid(row=0, column=0, sticky=tk.W + tk.E)

        # Define Vars
        self.rows_box_var = tk.IntVar()
        self.cols_box_var = tk.IntVar()
        self.table_rows_var = []
        self.filename, self.data = filename, data
        self.num_cols_data, self.num_rows_data = cols, rows

        self.build_main_gui()
        self.gui.mainloop()

    def build_main_gui(self):
        # Style
        self.style = ttk.Style()
        self.style.theme_use(self.style.theme_names()[1])

        self.manage_data()
        self.create_table_gui()
        self.create_widgets()
        self.create_menu()
        self.create_tool_bar()

    def create_tool_bar(self):

        ttk.Separator(self.toolbar_frame, orient=tk.VERTICAL).grid(row=0, column=4, padx=5, sticky=tk.N + tk.S + tk.W)
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        self.status_bar = ttk.Frame(self, border=1)  # , relief=tk.RIDGE)
        self.status_bar.grid(row=4, column=0, sticky=tk.W + tk.E)
        ttk.Label(self.status_bar,
                  text="Hello- I'm Status bar, here we are going to put some non-intersting data").grid()

    def create_menu(self):
        menu = tk.Menu(self.gui)
        self.gui.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New', command=self.rebuild_table)
        file_menu.add_command(label='Load ', command=self.load_button_callback)
        file_menu.add_command(label='Save', command=self.save_button)
        file_menu.add_command(label='Save as', command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.gui.destroy)

        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Size', command=self.load_button)

    def calc_size_data(self):
        # self.num_cols_data = min(self.num_cols_data,max([len(row) for row in self.data]))
        # self.num_rows_data = min(self.num_rows_data,len(self.data))
        self.rows_box_var.set(self.num_rows_data)
        self.cols_box_var.set(self.num_cols_data)

    def create_table_gui(self, rows=0, cols=0):
        # Canvas Min/default size (min/max for width and height)
        can_geometry = [200, 1000]

        # if size not defined- get data's size
        if rows == 0 and cols == 0:
            cols = self.num_cols_data
            rows = self.num_rows_data

        self.canvas = CanvasWidgets(self)
        self.canvas.grid(row=1, column=0)

        labels = self.create_letter_list(max(self.cols_box_var.get(), self.num_cols_data))
        # Create entries
        for r in range(rows + 1):
            self.m = []
            for c in range(cols + 1):
                if r == 0 and c < cols:
                    ttk.Label(self.canvas.frame, text=labels[c], font=('Helvetica', 8), relief=tk.FLAT).grid(row=r,
                                                                                                             column=c + 1)
                elif c == 0:
                    ttk.Label(self.canvas.frame, text=[r], font=('Helvetica', 8), relief=tk.FLAT).grid(row=r, column=c)
                elif r > 0 and c > 0:
                    self.m.append(tk.StringVar())
                    ent = ttk.Entry(self.canvas.frame, textvariable=self.m[-1], state=tk.NORMAL)
                    ent.grid(row=r, column=c)
                    #ent.bind('<Key>',self.insert_text)

            if r != 0 and c != 0:
                self.table_rows_var.append(self.m)

        self.canvas.frame.update()
        self.canvas.resize(w=max(can_geometry[0], min(can_geometry[1], self.canvas.frame.winfo_width())),
                           h=max(can_geometry[0], min(can_geometry[1] - 700, self.canvas.frame.winfo_height())))

        self.cols_box_var.set(cols)
        self.rows_box_var.set(rows)


        if not self.data == []:
            self.fill_table_gui()

        print("CSVGui - table created")

    def insert_text(event,self):
        pass

    def fill_table_gui(self):
        for r in range(self.num_rows_data):
            for col in range(self.num_cols_data):
                try:
                    self.table_rows_var[r][col].set(self.data[r][col])
                except IndexError:
                    pass
        print("CSVGui - Data entered to table")

    def create_widgets(self):
        self.save_button = ttk.Button(self.toolbar_frame, text='Save', command=self.save2file, width=5)
        self.save_button.grid(row=0, column=5)

        self.exit_button = ttk.Button(self.toolbar_frame, text='Exit', command=self.gui.destroy, width=5)
        self.exit_button.grid(row=0, column=7)

        self.load_button = ttk.Button(self.toolbar_frame, text='Load', command=self.load_button_callback, width=5)
        self.load_button.grid(row=0, column=6, padx=2)

        ttk.Label(self.toolbar_frame, text="Rows:").grid(row=0, column=0)

        self.rows_box = tk.Spinbox(self.toolbar_frame, width=5, from_=1, to=100, textvariable=self.rows_box_var,
                                   command=self.inc_rows_cols_callback)
        self.rows_box.grid(row=0, column=1)

        cols_label = ttk.Label(self.toolbar_frame, text="Columns:")
        cols_label.grid(row=0, column=2)
        self.cols_box = tk.Spinbox(self.toolbar_frame, width=5, from_=1, to=100, textvariable=self.cols_box_var,
                                   command=self.inc_rows_cols_callback)
        self.cols_box.grid(row=0, column=3)

    def inc_rows_cols_callback(self):
        # change dim of table - only if bigger than initial data
        if self.cols_box_var.get() >= self.num_cols_data and self.rows_box_var.get() >= self.num_rows_data:
            self.rebuild_table()
        elif self.cols_box_var.get() < self.num_cols_data:
            self.cols_box_var.set(self.num_cols_data)
        elif self.rows_box_var.get() < self.num_rows_data:
            self.rows_box_var.set(self.num_rows_data)

    def rebuild_table(self):
        self.canvas.destroy()
        self.table_rows_var = []
        self.create_table_gui(self.rows_box_var.get(), self.cols_box_var.get())

    def read_from_gui(self):
        minC, minR, maxR, maxC = 999999, 999999, 0, 0
        for r, rows in enumerate(self.table_rows_var):
            for c, cols in enumerate(rows):
                if cols.get() != '':
                    maxC = max(c, maxC)
                    maxR = max(r, maxR)
                    minR = min(r, minR)
                    minC = min(c, minC)

        parsed_data = []
        for r, row in enumerate(self.table_rows_var):
            if minR <= r <= maxR:
                parsed_data.append([])
                for c, col in enumerate(row):
                    if minC <= c <= maxC:
                        if col.get() == '':
                            parsed_data[-1].append('')
                        else:
                            parsed_data[-1].append(col.get())

        return parsed_data

    def save2file(self):
        if self.filename is '':
            self.filename = asksaveasfilename(defaultextension="*.*", title='Select CSV file',
                                              filetypes=[('CSV files', '.csv')])
        WriteFile('w', self.filename, data=self.read_from_gui())

    def save_as_file(self):
        self.filename = asksaveasfilename(defaultextension="*.*", title='Select CSV file',
                                          filetypes=[('CSV files', '.csv')])
        WriteFile('w', self.filename, data=self.read_from_gui())

    def load_file(self, fname=''):
        self.file = ReadFile(fname=fname)
        self.data = self.file.file_contents()
        self.filename = self.file.filename
        self.calc_size_data()

    def load_button_callback(self):
        self.load_file()
        self.rebuild_table()

    def clean_sheet(self):
        self.data = []

    def manage_data(self):
        #init_row_val = 10
        #init_col_val = 7

        if self.filename != '':
            self.load_file(fname=self.filename)
        # elif self.data == []:
        #     if self.num_cols_data == 0:
        #         self.num_cols_data = init_col_val
        #     if self.num_rows_data == 0:
        #         self.num_rows_data = init_row_val
        elif self.data != []:
            self.calc_size_data()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_letter_list(self, i):

        letter_list = []
        iters = 0
        while iters <= i:
            counter = divmod(iters, 26)
            if counter[0] > 0:
                letter_list.append(chr(ord('A') + counter[0] - 1) + chr(ord('A') + counter[1]))
            else:
                letter_list.append(chr(ord('A') + counter[1]))
            iters += 1
        return letter_list


class CanvasWidgets(ttk.Frame):
    def __init__(self, master, width=100, height=100):
        ttk.Frame.__init__(self, master)
        self.width, self.height = width, height
        self.frame = ttk.Frame(self)

        self.build_gui()

    def build_gui(self):
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='light green')
        self.frame.lift()
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.vsb.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W)
        self.hsb.grid(row=1, column=0, sticky=tk.W + tk.N + tk.E, columnspan=2)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.canvas.grid(row=0, column=0)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize(self, w, h):
        self.canvas.config(width=w, height=h)


class WriteFile:
    def __init__(self, args, fname, path='', data=[], headers=[]):

        if path != '':
            self.filename = path + '/' + fname
        else:
            self.filename = fname

        self.file_content = []
        self.save_file(args, data, headers)

    def save_file(self, args, data, headers):
        with open(self.filename, *args, newline='') as csvfile:
            file_obj = csv.writer(csvfile)
            file_obj.writerows(headers)
            file_obj.writerows(data)

        print("file %s was saved successfully, containing %d lines" % (self.filename, len(data) + len(headers)))

    def file_contents(self):
        return ReadFile(fname=self.filename).file_contents()

    def out_in_gui(self):
        ReadFile(fname=self.filename).out_in_gui()


#CSVGui()#data=[['a', 'c', 'b', 'f', 's'], ['a', 's', 'r', 't'], ['d', 5, 3, 'g', 6, ]])
# #b = WriteFile('w', '123.csv', 'd:/', data=[['a', 'c', 'b', 'f', 's'], ['a', 's', 'r', 't'], ['d', 5, 3, 'g', 6, ]],
#               headers=[['Guy', 'Dvir', 'Anna']])


# print(b.file_contents())
# ReadFile()
# print(ReadFile('123.csv', 'd:/').file_contents())
# b.out_in_gui()

# print(c.file_contents())
# c.out_in_gui()

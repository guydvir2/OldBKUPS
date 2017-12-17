import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import datetime
import socket
import time
import threading


class MainApp(ttk.Frame):
    def __init__(self, master=None, server='', logfile='', gui=True):
        ttk.Frame.__init__(self, master)

        self.txtvar = tk.StringVar()
        self.status_label_var, self.butvar = tk.StringVar(), tk.StringVar()
        self.max_con_label_var, self.max_discon_label_var = tk.StringVar(), tk.StringVar()
        self.tot_pings_var, self.recv_pings_var, self.lost_pings_var = tk.IntVar(), tk.StringVar(), tk.StringVar()
        self.cur_con_var = tk.StringVar()

        if gui:
            self.frame1 = ttk.Frame(self)
            self.frame1.grid(row=0, column=0)
            master.title("Where's my Internet ?")

            self.but_frame = ttk.LabelFrame(self, text="Select:", padding=5)
            self.but_frame.grid(row=0, column=1, sticky=tk.E + tk.W + tk.S, padx=5)
            self.statistics_frame = ttk.LabelFrame(self, text="Connection OverView", padding=5)
            self.statistics_frame.grid(row=1, column=0, columnspan=2, sticky=tk.E + tk.W + tk.N, padx=5, pady=5)
            self.menu_frame = ttk.Frame(self.frame1)
            self.menu_frame.grid(row=0, column=0)

            self.reset_parameters()

            self.py_file_location = sys.path[0]
            self.log_path = self.py_file_location
            self.log_filename = "wheresmyinternet.log"

            self.local_ip = socket.gethostbyname(socket.gethostname())

            self.build_gui()
            self.update_status_bar()
            self.update_log('App Start')

        else:
            pass

    def reset_parameters(self):
        self.timestamp = datetime.timedelta(0)
        self.time_vector = [datetime.timedelta(0)] * 4
        self.ping_vector = []
        self.state, self.elapsed_time = 0, '0'
        self.last_ping = -1
        # self.update_gui_pings()

    def build_gui(self):
        self.make_gui_menu()
        ttk.Label(self.frame1, text="Ping destination IP/URL:").grid(row=1, column=0, sticky=tk.W, padx=5)
        comb_vals = ['www.google.com', 'www.yahoo.com', '127.0.0.1', '10.53.5.253']
        ip_combo = ttk.Combobox(self.frame1, textvariable=self.txtvar, width=18, values=comb_vals)
        ip_combo.grid(row=1, column=1, pady=5)  # , sticky=tk.E)
        ip_combo.current(3)
        ip_combo.bind('<Return>', self.start_ping_callback)
        # ip_combo.bind('<Return>', self.start_ping_callback)

        # self.butvar.set("Start")
        ttk.Button(self.but_frame, text="Start", command=lambda arg='<>': self.start_ping_callback(arg)). \
            grid(row=0, column=0, sticky=tk.W + tk.E, columnspan=2, padx=5)

        ttk.Button(self.but_frame, text="Save Log", command=self.save_callback).grid(row=2, column=0, padx=5)
        ttk.Button(self.but_frame, text="Reset", command=self.reset_callback).grid(row=2, column=1, padx=5)
        ttk.Button(self.but_frame, text="Quit", command=self.exit_app). \
            grid(row=1, column=0, columnspan=2, sticky=tk.E + tk.W, padx=5, pady=5)

        self.textbox1 = tk.Text(self.frame1, height=10, font=(ip_combo.cget('font'), 8), width=45)
        self.textbox1.grid(row=2, column=0, columnspan=2, padx=5)
        self.yscrollbar = ttk.Scrollbar(self.frame1, orient=tk.VERTICAL)
        self.yscrollbar.grid(row=2, column=1, sticky=tk.N + tk.S + tk.E)
        self.textbox1.config(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.config(command=self.textbox1.yview)

        ttk.Label(self, textvariable=self.status_label_var, relief=tk.FLAT, anchor=tk.CENTER, justify=tk.CENTER). \
            grid(row=5, column=0, columnspan=5, sticky=tk.W + tk.E, padx=5)

        ttk.Label(self.statistics_frame, text="Current state. time: ").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.statistics_frame, text="Max Conn. time: ").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.statistics_frame, text="Max DisConn. time: ").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.statistics_frame, text="Total Pings: ").grid(row=0, column=3, sticky=tk.W)
        ttk.Label(self.statistics_frame, text="% Recv Pings: ").grid(row=1, column=3, sticky=tk.W)
        ttk.Label(self.statistics_frame, text="% Lost Pings: ").grid(row=2, column=3, sticky=tk.W)

        ttk.Label(self.statistics_frame, textvariable=self.tot_pings_var).grid(row=0, column=4, sticky=tk.W)
        ttk.Label(self.statistics_frame, textvariable=self.recv_pings_var, foreground='green'). \
            grid(row=1, column=4, sticky=tk.W)
        ttk.Label(self.statistics_frame, textvariable=self.lost_pings_var, foreground='red'). \
            grid(row=2, column=4, sticky=tk.W)

        ttk.Label(self.statistics_frame, textvariable=self.cur_con_var, width=25).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(self.statistics_frame, textvariable=self.max_con_label_var).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(self.statistics_frame, textvariable=self.max_discon_label_var).grid(row=2, column=1, sticky=tk.W)

    def make_gui_menu(self):
        menu = tk.Menu(root)
        root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label='Exit', command=self.exit_app)
        file_menu.add_command(label='Shitt')

        menu.add_cascade(label='File', menu=file_menu)

        log_menu = tk.Menu(menu, tearoff=0)
        log_menu.add_command(label='File location', command=self.file_location)
        log_sub_menu = tk.Menu(log_menu)
        log_sub_menu.add_radiobutton(label='Overwrite file')
        log_sub_menu.add_radiobutton(label='Append to file')
        log_menu.add_cascade(label='Overwrite/ Append log', menu=log_sub_menu)

        menu.add_cascade(label='Log', menu=log_menu)

    def update_status_bar(self):
        clock = datetime.datetime.now()
        self.elapsed_time = str(self.time_vector[2] + self.time_vector[3]).split('.')[0]
        self.status_label_var.set(
            str(clock).split('.')[0] + ", Elapsed: " + self.elapsed_time + ', Local IP: ' + str(self.local_ip))

        self.after(1000, self.update_status_bar)

    def update_log(self, input):
        self.textbox1.insert(tk.END, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + input + '\n')

    # def start_ping_callback(self, event, address=''):
    #
    #     def run_ping():
    #         ping_result = os.system('ping %s -n 1  >NULL' % address)
    #         self.ping_vector.append(ping_result)
    #
    #         round_time_qouta = datetime.datetime.now() - self.timestamp
    #         self.timestamp = datetime.datetime.now()
    #
    #         self.update_time_counter(ping_result, round_time_qouta)
    #         self.update_ping_counter(color='green')
    #
    #         if self.last_ping != ping_result:
    #             text = ['Reachable', 'Lost']
    #             self.update_log("%s %s" % (address, text[ping_result]))
    #
    #         self.last_ping = ping_result
    #         self.root_id = root.after(2000, run_ping)
    #
    #     if address == '':
    #         address = self.txtvar.get()
    #
    #     # Start Pressed
    #     if self.state == 0:
    #         self.timestamp = datetime.datetime.now()
    #         self.butvar.set("Stop")
    #         self.update_log("Start pinging %s" % address)
    #         self.status_label.focus()
    #         run_ping()
    #         self.state = 1
    #     # Stop Pressed
    #     elif self.state == 1:
    #         self.stop_ping()
    #
    def start_ping_callback(self, event, address=''):
        # Background Thread
        self.Pinger = Pinger(address=self.txtvar.get())
        self.Pinger.start()
        self.update_gui_pings()

    def update_gui_pings(self):
        # print(self.Pinger.get_status())
        res = self.Pinger.get_status()

        if res[1] != [0, 0]:
            recv_ratio = res[1][0] / (res[1][0] + res[1][1])
            lost_ratio = 1 - recv_ratio
        else:
            recv_ratio = 0
            lost_ratio = 0

        self.tot_pings_var.set(res[1][0] + res[1][1])
        self.recv_pings_var.set("%.1f" % (recv_ratio * 100) + "%")
        self.lost_pings_var.set("%.1f" % (lost_ratio * 100) + "%")

        if res[0] != []:
            if res[0][0] == 0:
                self.cur_con_var.set(str("Recv- ") + str(res[0][1]))
                self.max_con_label_var.set(max(self.max_con_label_var.get(), res[0][2]))
            elif res[0][0] == 1:
                self.cur_con_var.set(str("Lost- ") + str(res[0][1]))
                self.max_discon_label_var.set(max(self.max_discon_label_var.get(), res[0][2]))

        self.after(500, self.update_gui_pings)

    #
    # def update_time_counter(self, ping_result=0, time_quota=datetime.timedelta(0)):
    #     """self.time_vector = [[cons.succ ping time],[cons.not_succ ping time],
    #     [max accum succ ping time],[max accum not_succ ping time] """
    #
    #     p_vec = [0, 1]
    #
    #     self.time_vector[p_vec[ping_result]] += time_quota
    #     if self.time_vector[p_vec[ping_result]].total_seconds() > self.time_vector[
    #         p_vec[ping_result] + 2].total_seconds():
    #         self.time_vector[p_vec[ping_result] + 2] = self.time_vector[p_vec[ping_result]]
    #
    #     self.time_vector[p_vec[ping_result - 1]] = datetime.timedelta(0)
    #
    #     # GUI update
    #     color_list = ['green', 'red']
    #     state = [' (connected)', ' (not connected)']
    #     self.cur_con_label["foreground"] = color_list[ping_result]
    #     self.cur_con_var.set(str(self.time_vector[ping_result]).split('.')[0] + state[ping_result])
    #     self.max_con_label_var.set(str(self.time_vector[2]).split('.')[0])
    #     self.max_discon_label_var.set(str(self.time_vector[3]).split('.')[0])
    #
    # def stop_ping(self):
    #     self.butvar.set("Start")
    #     root.after_cancel(self.root_id)
    #     self.update_log("Stopped by User")
    #     self.state = 0

    def reset_callback(self):
        if self.state == 0:
            self.textbox1.delete(2.0, tk.END)
            self.textbox1.insert(2.0, '\n')
            self.reset_parameters()
            self.cur_con_var.set("")
            self.cur_con_label["foreground"] = 'black'
            self.max_con_label_var.set("")
            self.max_discon_label_var.set("")

    def save_callback(self):
        content = (self.textbox1.get(1.0, tk.END))
        statistic1 = 'Current state time:%s\nMax Conection time:%s\nMax disconnection time:%s\n' % (
            self.cur_con_var.get(), self.max_con_label_var.get(), self.max_discon_label_var.get())
        statistic2 = 'Total pings:%s\n%% Reach ratio:%s\n%% Lost ratio:%s' % (
            self.tot_pings_var.get(), self.recv_pings_var.get(), self.lost_pings_var.get())

        str1 = "File saved in %s\n" % (str(datetime.datetime.now())).split('.')[0]
        with open(self.log_path + '/' + self.log_filename, "a") as text_file:
            text_file.write(str1 + '#' * len(
                str1) + '\n' + content + '\n' + statistic1 + '\n' + statistic2 + '\n\n' + self.status_label_var.get() + '\n\n')
        self.update_log('log saved')

    def file_location(self):
        temp_loc = filedialog.askdirectory(title='Select folder for Log file')
        if not temp_loc == '': self.log_path = temp_loc

    def exit_app(self):
        if tkinter.messagebox.askyesno("Please Confirm", 'Continue with Exit ?'):
            root.destroy()
            self.Pinger.stop()


class Pinger(threading.Thread):
    def __init__(self, address='', ping_rate=5, del_time_notify=10, test_period=None, log_filename='PingerLog.txt'):
        threading.Thread.__init__(self)
        # os.system('taskkill /f /im PING.exe')

        self.address, self.logname = address, log_filename
        self.ping_rate, self.test_period = ping_rate, test_period
        self.ping_vector, self.last_ping, self.last_ping_output = [], -1, ''
        self.del_time_notify, self.last_notify_time = del_time_notify, datetime.timedelta(0)
        self.start_time, self.last_status = datetime.datetime.now(), []
        self.timestamp, self.time_vector, self.accum_time_vector = 0, [datetime.timedelta(0)] * 4, \
                                                                   [datetime.timedelta(0)] * 2
        self.event = threading.Event()
        self.pings_counter = [0, 0]
        self.fail_pings, self.recv_pings = 0, 0

        self.log2file("\n~~~~~~~~~~ Start Ping to:%s ~~~~~~~~~~\n" % self.address)

    def run(self):
        self.timestamp = datetime.datetime.now()
        while not self.event.is_set():
            self.start_ping()

            # Check if test period is over
            if self.test_period != None and (self.timestamp - self.start_time).total_seconds() >= self.test_period:
                a = self.get_status()
                a[1] = [' End ']
                self.log2file(str([a[0], a[1], a[2], a[5], a[6], a[7]]))
                self.stop()
            else:
                pass
            self.event.wait(self.ping_rate)

    def stop(self):
        self.event.set()

    def start_ping(self):
        ping_result = os.system('ping %s -n 1 >NULL' % self.address)
        self.ping_vector.append(ping_result)

        if self.last_ping != ping_result:
            text = ['Reachable', 'Lost']
            # print(str(self.timestamp)[:-4], self.address, text[ping_result])

        round_time_qouta = datetime.datetime.now() - self.timestamp
        self.timestamp = datetime.datetime.now()
        self.update_time_counter(ping_result, round_time_qouta)

        self.last_ping = ping_result

    def update_time_counter(self, ping_result=0, time_quota=datetime.timedelta(0)):
        """self.time_vector = [[cons.succ ping time],[cons.not_succ ping time],
        [max accum succ ping time],[max accum not_succ ping time] """

        def display_status():
            self.last_notify_time = datetime.datetime.now()
            recv_ratio = self.accum_time_vector[0].total_seconds() / \
                         (self.accum_time_vector[0].total_seconds() + self.accum_time_vector[1].total_seconds())
            lost_ratio = 1 - recv_ratio
            self.last_ping_output = [str(self.timestamp)[:-4], prefix, "State: " + ['Received', 'Lost'][ping_result],
                                     " Duration: " + self.last_status[1], " Max Duration: " + self.last_status[2],
                                     "Elapsed time: " + self.last_status[3], 'Recv ratio: %.1f%%' % (recv_ratio * 100),
                                     'Lost ratio: %.1f%%' % (lost_ratio * 100)]

            return self.last_ping_output

        p_vec = [0, 1]
        last_ping = -1

        if self.last_status != []: last_ping = self.last_status[0]

        self.pings_counter[ping_result] += 1
        self.time_vector[p_vec[ping_result]] += time_quota
        self.accum_time_vector[p_vec[ping_result]] += time_quota

        if self.time_vector[p_vec[ping_result]].total_seconds() > \
                self.time_vector[p_vec[ping_result] + 2].total_seconds():
            self.time_vector[p_vec[ping_result] + 2] = self.time_vector[p_vec[ping_result]]

        self.time_vector[p_vec[ping_result - 1]] = datetime.timedelta(0)
        self.last_status = [ping_result, self.chop_milisecond(self.time_vector[ping_result]),
                            self.chop_milisecond(self.time_vector[ping_result + 2]),
                            self.chop_milisecond(datetime.datetime.now() - self.start_time)]

        # Notify Status
        if last_ping == -1:
            prefix = ' [ Start ] '
            print(display_status())
            self.log2file(str(display_status()))
        elif self.last_status[0] != last_ping:
            prefix = ' [ Change ] '
            print(display_status())
            self.log2file(str(display_status()))
        elif datetime.datetime.now() - self.last_notify_time > datetime.timedelta(seconds=self.del_time_notify):
            prefix = ' [ Period ] '
            print(display_status())
            self.log2file(str(display_status()))

    @staticmethod
    def chop_milisecond(time1):
        return str(time1).split('.')[0]

    def get_status(self):
        return self.last_ping_output  # self.last_status, self.pings_counter

    def log2file(self, logtext=''):
        with open(self.logname, "a") as log:
            log.write(logtext + '\n')


c = Pinger('10.53.5.253', ping_rate=2, test_period=60, del_time_notify=3)
c.start()
# time.sleep(20)
# c.stop()

# root = tk.Tk()
# app = MainApp(root, gui=True)
# app.grid()
# root.mainloop()

# from platform import system as system_name # Returns the system/OS name
# from os import system as system_call       # Execute a shell command
#
# def ping(host):
#     """
#     Returns True if host (str) responds to a ping request.
#     Remember that some hosts may not respond to a ping request even if the host name is valid.
#     """
#
#     # Ping parameters as function of OS
#     parameters = "-n 1" if system_name().lower()=="windows" else "-c 1"
#
#     # Pinging
#     return system_call("ping " + parameters + " " + host) == 0
#
# ping('127.0.0.1')

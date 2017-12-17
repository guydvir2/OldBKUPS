import tkinter as tk
import gpiozero
from time import sleep
import time
from gpiozero import OutputDevice
# from gpiozero.pins.pigpio import PiGPIOFactory
import datetime
from tkinter import ttk
# import Schedule
# import csv
import os


class ScheduledEvents:
    def __init__(self, master=None, tasks=[], task_stat=[], label_1=[], sw=0):

        self.master = master
        self.tasks = tasks
        self.label = label_1
        self.task_state = task_stat
        self.sw = sw
        self.result_vector, self.future_on = [0] * len(self.tasks), [0] * len(self.tasks)

        if self.check_integrity_time_table() == 0:
            self.run_schedule()
        else:
            print("Errors in TimeTable")
        self.switch_descision()

    def check_integrity_time_table(self):
        time_err, days_err = 0, 0

        for i in range(len(self.tasks)):
            time1 = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
            time2 = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()

            for day_in_task in self.tasks[i][0]:
                if not day_in_task in range(1, 8):
                    print("day of task %d is not valid" % i)
                    days_err += 1

                if not time2 > time1:
                    print("Time interval of task %d is not valid" % i)
                    time_err += 1

        if time_err + days_err == 0:
            return 0  # No Errors
        else:
            return 1  # Errors on TimeTable

    def run_schedule(self):

        def time_diff(t1):
            t2 = datetime.datetime.now().time()
            today1 = datetime.date.today()
            return datetime.datetime.combine(today1, t1) - datetime.datetime.combine(today1, t2)

        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)

        for i in range(len(self.tasks)):
            self.result_vector[i] = [2] * len(self.tasks[i][0])
            self.future_on[i] = [2] * len(self.tasks[i][0])

        for i in range(len(self.tasks)):  # Total tasks
            for m, day_in_task in enumerate(self.tasks[i][0]):  # days in same task
                day_diff = day_in_task - datetime.datetime.today().isoweekday()

                # Today
                if day_in_task == datetime.date.today().isoweekday():
                    start_time = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
                    stop_time = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()

                    # Before Time
                    if start_time > datetime.datetime.now().time():
                        self.result_vector[i][m] = -1

                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(day_diff),
                                                             datetime.datetime.strptime(self.tasks[i][1],
                                                                                        '%H:%M:%S').time())
                        # print("b4")


                    # In Time
                    elif start_time < (datetime.datetime.now() - datetime.timedelta(seconds=1)).time() and (
                                datetime.datetime.now() + datetime.timedelta(seconds=1)).time() < stop_time:
                        self.result_vector[i][m] = 1

                        new_date = datetime.datetime.combine(datetime.date.today(),
                                                             datetime.datetime.strptime(self.tasks[i][2],
                                                                                        '%H:%M:%S').time())
                        # print("innnn")

                    # Time to Off
                    elif (datetime.datetime.now() + datetime.timedelta(
                            seconds=2)).time() > stop_time and datetime.datetime.now().time() < stop_time:
                        self.result_vector[i][m] = 0
                        # print("offff")

                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7),
                                                             datetime.datetime.strptime(self.tasks[i][1],
                                                                                        '%H:%M:%S').time())

                    # Byond Command Times
                    else:
                        self.result_vector[i][m] = -1

                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7),
                                                             datetime.datetime.strptime(self.tasks[i][1],
                                                                                        '%H:%M:%S').time())



                # Day in Future
                elif day_in_task > datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1

                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta
                    (day_diff), datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())


                # Day in Past, Next in Future
                elif day_in_task < datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1

                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7 + day_diff),
                                                         datetime.datetime.strptime(self.tasks[i][1],
                                                                                    '%H:%M:%S').time())

                self.future_on[i][m] = chop_microseconds(new_date - datetime.datetime.now())

        return self.get_status()

    def get_status(self):
        ans = [-1, -1]
        min_time = []

        for x, res_vec in enumerate(self.result_vector):
            min_time.append(min(self.future_on[x]))
            for op in res_vec:
                if op in [0, 1]:
                    ans = [op, x]  # op state = on/off x= task number
        print([ans, min_time, min(min_time)])
        return [ans, min_time, min(min_time)]  # , self.future_on]

    def switch_descision(self):
        # Check what Sched vector are supplied:
        def check_state(sch_stat, task_stat, label_1, sw):
            # sw  to pass to x_switch method
            # Switch On/Off -------** **-----in task no.     relative task_state is On -------_**

            if not sch_stat[0][0] == -1 and task_stat[sch_stat[0][1]] == 1:
                if not bool(sch_stat[0][0]) == self.master.get_state()[sw]:
                    self.master.ext_press(sw, sch_stat[0][0], "Schedule Switch")
                    # Which button to switch--^^   on or off ----^^

            # Reset task status after sched end ( in case it was cancelled )
            elif sch_stat[0][0] == -1 and task_stat[sch_stat[0][1]] == 0:
                task_stat[sch_stat[0][1]] == 1

            # if in "On" state : show time left to "On"
            if sch_stat[0][0] == 1 and task_stat[sch_stat[0][1]] == 1:
                # label_1.set("'%s' OFF :\n"%sw_txt[sw] + str(sch_stat[2]))
                label_1.set(str(sch_stat[2]))
            # if in "off state": time to next on, in all tasks
            elif sch_stat[0][0] == -1:
                # label_1.set("'%s' ON :\n"%sw_txt[sw] + str(sch_stat[2]))
                label_1.set(str(sch_stat[2]))
            elif sch_stat[0][0] == 1 and task_stat[sch_stat[0][1]] == 0:
                label_1.set("Task %s, canclled" % str(sch_stat[0][1]))

        sched_status = self.run_schedule()
        check_state(sched_status, self.task_state, self.label, self.sw)
        self.master.after(500, self.switch_descision)


class LongPressButton(tk.Frame):
    def __init__(self, master=None, remote=0, time=0):
        tk.Frame.__init__(self, master)
        self.but_var = tk.StringVar()
        self.ent_var = tk.StringVar()
        self.lbl_var = tk.StringVar()
        self.style = ttk.Style()
        self.on = False

        if remote == 1:  # Use without GUI, as counter only
            self.remote = 1
            self.build_gui(gui='no')
            self.restart()

        elif not remote == 1:
            self.build_gui()
            self.restart()

    def restart(self):
        self.update_ent("Enter", 'blue')
        self.tic, self.toc = 0, 0
        self.on_off_status = 0
        self.but_var.set("Start")
        self.lbl_var.set('End time: ')

    def build_gui(self, gui=''):

        if gui == 'yes':  # GUI is on
            self.button = ttk.Button(self, textvariable=self.but_var, command=self.read_time)
            self.button.grid(row=0, column=1)
            self.button.bind('<Button-1>', self.press_but)
            self.button.bind('<ButtonRelease-1>', self.release_but)

            self.label = ttk.Label(self, textvariable=self.lbl_var, relief=tk.RIDGE, anchor=tk.N)
            self.label.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

        self.entry = ttk.Entry(self, textvariable=self.ent_var, justify=tk.CENTER, width=15)
        self.entry.bind('<Button-1>', self.clear_ent)
        self.entry.grid(row=0, column=0)

    def press_but(self, event):

        if self.on:
            print('stop')
            self.but_var.set('Cont.')
            self.after_cancel(self.a)
            self.on = False
        elif not self.on:
            print('press start')
            self.but_var.set('Stop')
            self.on = True

        self.tic = time.time()

    def release_but(self, event):

        self.toc = time.time() - self.tic
        print(self.toc)
        self.tic = 0

    def validate_time(self, time_input):
        timeformat = "%H:%M:%S"
        try:
            validtime = datetime.datetime.strptime(time_input, timeformat)
            a = validtime.timetuple()
            b = datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).total_seconds()
            # print('Valid time format')
            return b
        except ValueError:
            # print("invalid time format")
            return None

    def read_time(self):

        if self.toc > 0.5:
            print("long press")
            self.succ_end()
        else:
            if self.on:
                try:
                    if type(int(self.ent_var.get())) is int:
                        b = int(self.ent_var.get())
                        self.time_out(seconds=int(self.ent_var.get()))
                        t = (datetime.datetime.now() + datetime.timedelta(seconds=int(b))).strftime("%Y-%m-%d %H:%M:%S")
                        self.lbl_var.set('End time: ' + str(t))
                        if len(self.ent_var.get()) > self.entry.cget('width'):
                            self.entry["width"] = len(self.ent_var.get())
                except ValueError:
                    time1 = self.validate_time(self.ent_var.get())
                    if time1 is not None:
                        t = (datetime.datetime.now() + datetime.timedelta(seconds=int(time1))).strftime(
                            "%Y-%m-%d %H:%M:%S")
                        self.lbl_var.set('End time: ' + str(t))
                        self.time_out(seconds=time1)
                    else:
                        if not self.ent_var.get() == 'Enter':
                            self.update_ent("Bad format", 'red')
                            # time.sleep(2)
                            # self.restart()

    def time_out(self, days=0, seconds=0):

        def update_clock():
            time_left = future - datetime.datetime.now()
            if time_left.total_seconds() > 0:
                time_str = str(time_left).split('.')[0]
                self.ent_var.set(time_str)
                self.on_off_status = 1
                self.a = self.after(500, update_clock)
            else:
                self.on_off_status = 0
                self.succ_end()

            if self.remote == 1: self.master.ext_press(0, self.on_off_status, "TimeOut Switch")

        now = datetime.datetime.now()
        future = now + datetime.timedelta(days, seconds)
        update_clock()

    def update_ent(self, text, color='black'):
        self.style.configure('Guy.TEntry', foreground=color)
        self.entry['style'] = 'Guy.TEntry'
        self.ent_var.set(text)

    def clear_ent(self, event):
        if type(self.ent_var.get()) is str:
            self.ent_var.set('')

    def succ_end(self):
        try:
            self.after_cancel(self.a)
            self.restart()
        except AttributeError:
            pass
        self.on = False
        self.restart()


class Indicators:
    # This Calss displays output state of GPIO
    def __init__(self, master, frame, num_indic=2):
        self.master = master
        self.frame = frame
        self.t = num_indic  # Amount of indicators needed
        self.indicators = ['indicator' + str(i) for i in range(self.t)]
        self.build_gui()
        self.update_indicators()

    def update_indicators(self):
        for i in range(self.t):
            if self.master.get_state()[i] == False:
                self.indicators[i].config(bg="red")
            elif self.master.get_state()[i] == True:
                self.indicators[i].config(bg="green")

        self.frame.after(500, self.update_indicators)

    def build_gui(self):
        # create indicators ( label changes color)
        ofset = 0
        for i in range(self.t):
            self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue', relief=tk.SUNKEN)
            self.indicators[i].grid(row=i, column=0, sticky=tk.E, pady=ofset, padx=3)


class HWRemoteInput:
    # This class create a link between input_pins(HW buttons) to output pins
    def __init__(self, master, ip, input_pins):
        self.master = master
        factory = PiGPIOFactory(host=ip)

        self.input_pins = ["Pin_" + str(input_pins[i]) for i in range(len(input_pins))]
        for sw in range(len(self.input_pins)):
            self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
            self.input_pins[sw].when_pressed = lambda arg=sw: self.pressed(arg)

        print("RemoteInput Init-%s, IP:%s, GPIO pins:%s" % (self.master.nick, ip, input_pins))

    # Detect press and make switch
    def pressed(self, i):
        self.master.switch_type = 'HWButton Switch'
        # self.master.HW_Button(i, [1, 0][self.master.HW_output.get_state()[i]])
        self.master.ext_press(i, [1, 0][self.master.HW_output.get_state()[i]], "HWButton")

    def get_state(self):
        stat = []
        for sw in (self.input_pins):
            stat.append([sw.value])
        return stat


class HWRemoteOutput:
    # This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
    def __init__(self, master, ip, output_pins):
        self.master = master
        factory = PiGPIOFactory(host=ip)
        self.output_pins = ["Pin_" + str(output_pins[i]) for i in range(len(output_pins))]
        for sw in range(len(self.output_pins)):
            self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory, initial_value=False)

        print("RemoteOutput Init %s, IP:%s, GPIO pins:%s" % (self.master.nick, ip, output_pins))

    # Make the switch
    def set_state(self, sw, state):
        if state == 1:
            self.output_pins[sw].on()
        elif state == 0:
            self.output_pins[sw].off()

            # Inquiry

    def get_state(self):
        stat = []
        for sw in range(len(self.output_pins)):
            stat.append(self.output_pins[sw].value)
        return stat


class UpDownButton(tk.Frame):
    def __init__(self, master, nickname='', text_up='UP', text_down='DOWN', width=15, height=3, hw_in=[], hw_out=[],
                 ip_in='', ip_out='', sched_vector=[], sched_vector_down=[]):

        tk.Frame.__init__(self, master)
        self.nick = nickname
        self.master = master
        self.text_up = text_up
        self.text_down = text_down
        self.status_label_up_var = tk.StringVar()
        self.status_label_up_var.set('Status: None')
        self.status_label_down_var = tk.StringVar()
        self.status_label_down_var.set('Status: None')
        self.but_stat = []
        self.switch_type = ''
        self.up, self.down = 0, 0
        sched_vector_up = sched_vector  # to keep comm with other buttons ( for now )
        if ip_in == '': ip_in = ip_out  # in case remote input is not defined

        self.build_gui(text_up, text_down, width, height)

        # self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        # Indicators(self.HW_output, self)
        # if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)

        if not sched_vector_up == []:
            # sched_vector = [[1,"22:00:40","23:24:10"]]
            self.task_state_up = [1] * len(sched_vector_up)
            self.SchRun_Up = ScheduledEvents(self, tasks=sched_vector_up, task_stat=self.task_state_up,
                                             label_1=self.status_label_up_var, sw=0)
            self.up = 1

        if not sched_vector_down == []:
            self.task_state_down = [1] * len(sched_vector_down)
            self.SchRun_Down = ScheduledEvents(tasks=sched_vector_down)
            self.down = 1

            # if self.up or self.down > 0: self.run_schedule()

    def build_gui(self, text_up, text_down, width, height):

        but1_var = tk.IntVar()
        but1 = tk.Checkbutton(self, text=text_up, width=width, height=height, indicatoron=0, variable=but1_var,
                              command=lambda: self.sf_button_press(0))
        but1.grid(row=0, column=0, pady=5)

        but2_var = tk.IntVar()
        but2 = tk.Checkbutton(self, text=text_down, width=width, height=height, indicatoron=0, variable=but2_var,
                              command=lambda: self.sf_button_press(1))
        but2.grid(row=1, column=0)

        label = tk.Label(self, text=self.nick, fg='red')
        label.grid(row=2, column=0)

        sepr1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        sepr1.grid(row=3, column=0, sticky=tk.E + tk.W)

        self.status_label_up = tk.Label(self, textvariable=self.status_label_up_var, relief=tk.SUNKEN,
                                        font=("Helvetica", 7))
        self.status_label_up.grid(row=0, column=0, sticky=tk.S, pady=7)

        self.status_label_down = tk.Label(self, textvariable=self.status_label_down_var, relief=tk.SUNKEN,
                                          font=("Helvetica", 7))
        self.status_label_down.grid(row=1, column=0, sticky=tk.S, pady=3)

        self.but_stat = [but1_var, but2_var]

    def switch_logic(self, sw):

        sw_i = [0, 1]
        if self.but_stat[sw_i[sw]].get() == 1:  # Pressed to turn on
            if self.but_stat[sw_i[sw - 1]].get() == 1:  # check if pther is on
                self.but_stat[sw_i[sw - 1]].set(0)  # turn other off
                self.execute_command(sw_i[sw - 1], 0, 'Logic Switch')  # turn other off
                sleep(1)
                self.execute_command(sw_i[sw], 1)  # turn on

            elif self.but_stat[sw_i[sw - 1]].get() == 0:  # if other is off
                self.execute_command(sw_i[sw], 1)  # turn on

        elif self.but_stat[sw_i[sw]].get() == 0:  # if pressed to turn off
            self.execute_command(sw_i[sw], 0)  # turn off

    def sf_button_press(self, sw):
        self.switch_type = 'SFButton Switch'
        self.switch_logic(sw)
        self.disable_sched_task()

    def ext_press(self, sw, state, type_s):
        self.switch_type = type_s
        self.but_stat[sw].set(state)
        self.switch_logic(sw)
        if not type_s == "Schedule Switch":
            self.disable_sched_task()

    def disable_sched_task(self):
        # Stop Schedule run if it was defined at start
        try:  # if there is a schedule
            # if schedule in ON- disable it for next run
            if not self.SchRun_Up.get_status()[0][0] == -1:
                self.task_state_up[self.SchRun_Up.get_status()[0][1]] = 0
                print("Task: Disabled")  # ^^------toggle button
            if not self.SchRun_Down.get_status()[0][0] == -1:
                self.task_state_down[self.SchRun_Down.get_status()[0][1]] = 0
                print("Task: Disabled")  # ^^------toggle button
        except AttributeError:
            # No schedule to stop
            pass

    def execute_command(self, sw, stat, add_txt=''):

        # self.HW_output.set_state(sw, stat)
        print([self.nick, self.switch_type, 'Up is:' + str('self.HW_output.get_state()[0]'),
               'Down is: ' + str('self.HW_output.get_state()[1]'), add_txt])

    def get_state(self):
        return self.HW_output.get_state()


class ToggleButton(tk.Frame):
    def __init__(self, master, nickname='ToggleButton', height=3, width=15, ip_in='', hw_in=[], ip_out='', hw_out=[],
                 sched_vector=[]):

        tk.Frame.__init__(self, master)
        if ip_in == '': ip_in = ip_out
        self.nick = nickname
        self.master = master
        self.label_var = tk.StringVar()
        self.label2_var = tk.StringVar()
        self.txtvar = tk.StringVar()
        self.but_var = tk.IntVar()
        self.but_stat = []  # tk.IntVar()

        # self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        # Indicators(self.HW_output, self, 1)
        # if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)


        self.build_gui(self, nickname, height, width)
        self.switch_type = ''
        self.last_exec = ''
        self.task_state = [1] * len(sched_vector)

        self.Counter = LongPressButton(self, remote=1)
        self.Counter.grid(row=2, column=0)

        if not sched_vector == []:
            # sched_vector = [[1,"22:00:40","23:24:10"]]
            self.SchRun = ScheduledEvents(self, tasks=sched_vector, task_stat=self.task_state, label_1=self.label2_var)

    def build_gui(self, master, nickname, height, width):

        button = tk.Checkbutton(self, text=nickname, variable=self.but_var, indicatoron=0, height=height, width=width,
                                command=self.sf_button_press)
        button.grid(row=0, column=0, padx=3)

        self.label = tk.Label(self, textvariable=self.label_var)
        self.label.grid(row=2, column=0)

        self.label2 = tk.Label(self, textvariable=self.label2_var)
        self.label2.grid(row=3, column=0)

        self.but_stat = [self.but_var]

    def switch_logic(self, sw):
        if self.but_stat[sw].get() == 0:
            self.Counter.succ_end()
        # print(self.Counter.on_off_status)
        pass

    def sf_button_press(self, sw=0):
        # sw=0 - 1 button only
        self.switch_type = 'SFButton Switch'
        self.Counter.on = self.but_stat[sw].get()
        self.Counter.read_time()
        self.switch_logic(sw)
        self.disable_sched_task()

    def ext_press(self, sw, state, type_s):
        self.switch_type = type_s
        self.but_stat[sw].set(state)
        self.switch_logic(sw)
        if not type_s == "Schedule Switch":
            self.disable_sched_task()
            # print("EXT_SCD")

    def disable_sched_task(self):
        # Stop Schedule run if it was defined at start
        try:  # if there is a schedule
            # if schedule in ON- disable it for next run
            if not self.SchRun.get_status()[0][0] == -1:
                self.task_state[self.SchRun.get_status()[0][1]] = 0
                print("Task: Disabled")  # ^^------toggle button
        except AttributeError:
            # No schedule to stop
            pass

    def execute_command(self, sw, stat, add_txt=''):

        # self.HW_output.set_state(sw, stat)
        print([self.nick, self.switch_type, 'Up is:' + str('self.HW_output.get_state()[0]'),
               'Down is: ' + str('self.HW_output.get_state()[1]'), add_txt])

    def get_state(self):
        return self.HW_output.get_state()


class MainsButton(tk.Frame):
    # class HWRemoteOutput:
    ##This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
    # def __init__(self,master, ip, output_pins):
    # factory = PiGPIOFactory(host=ip)
    # self.master = master
    # self.output_pins= ["Pin_"+str(output_pins[i]) for i in range(len(output_pins))]
    # for sw in range(len(self.output_pins)):
    # self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory,initial_value=False)

    # print("RemoteOutput Init %s, IP:%s, GPIO pins:%s"%(self.master.nick, ip, output_pins))


    ##Make the switch
    # def set_state(self, sw, state):
    # if state == 1:
    # self.output_pins[sw].on()
    # elif state == 0:
    # self.output_pins[sw].off()

    ##Inquiry
    # def get_state(self):
    # stat=[]
    # for sw in range(len(self.output_pins)):
    # stat.append(self.output_pins[sw].value)
    # return stat


    # class Indicators:

    # def __init__(self,master, frame ):
    # self.master = master
    # self.frame = frame
    # self.t = 2 # Amount of indicators/ switches
    # self.indicators = ['indicator'+str(i) for i in range(self.t)]
    # self.build_gui()
    # self.update_indicators()


    # def update_indicators(self):
    # for i in range(self.t):
    # if str(self.master.get_state()[i]) == "False":
    # self.indicators[i].config(bg="red")
    # elif str(self.master.get_state()[i]) == "True":
    # self.indicators[i].config(bg="green")
    # self.frame.after(500, self.update_indicators)


    # def build_gui(self):
    # ofset=8
    # for i in range(self.t):
    # self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue',relief=tk.SUNKEN)
    # self.indicators[i].grid(row=i, column=0, sticky=tk.NE, pady=ofset, padx=ofset)


    # class HWRemoteInput:
    ##This class create a link between input_pins(HW buttons) to output pins
    # def __init__(self, master, ip, input_pins):
    # self.master = master
    # factory = PiGPIOFactory(host=ip)

    # self.input_pins= ["Pin_"+str(input_pins[i]) for i in range(len(input_pins))]
    # for sw in range(len(self.input_pins)):
    # self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
    # self.input_pins[sw].when_pressed = lambda arg=sw :self.pressed(arg)

    # print("RemoteInput Init-%s, IP:%s, GPIO pins:%s"%(self.master.nick,ip, input_pins))

    ##Detect press and make switch
    # def pressed(self,i):
    # self.master.switch_type = 'HWButton Switch'
    # self.master.HWbutton_pressed(i,[1,0][self.master.HW_output.get_state()[i]])

    # def get_state(self):
    # stat=[]
    # for sw in range(len(self.input_pins)):
    # stat.append([self.input_pins[sw].value])
    # return stat


    def __init__(self, master, nickname='MainsBut', ip_out='192.168.2.113', hw_out=[4, 27], hw_in=[21, 22],
                 ip_in='192.168.2.113', sched_vector=[[[4, 5, 6], "06:00:40", "23:24:10"]], height=3, width=15):

        tk.Frame.__init__(self, master)
        self.mainframe = ttk.Frame(self)
        self.master = master
        self.nick = nickname
        self.allow_to_switch = 0

        self.build_buttons(width, height)
        self.switch_type = ''
        self.last_exec = ''
        self.task_state = [1] * len(sched_vector)

        # Using GIO HW classes
        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        Indicators(self.HW_output, self)
        if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)
        if not sched_vector == []:
            # sched_vector = [[1,"22:00:40","23:24:10"]]
            self.SchRun = ScheduledEvents(tasks=sched_vector)
            self.run_schedule()

    def build_buttons(self, width, height):

        def restore_timeout(event):
            if not self.txtvar.get() == self.init_var:
                try:
                    int(self.txtvar.get())
                except ValueError:
                    self.txtvar.set(self.init_var)

        def clear_timeout(event):
            self.txtvar.set("")

        self.init_var = "TimeOut [min]"

        self.txtvar = tk.StringVar()
        self.txtvar.set(self.init_var)
        timeout_entry = tk.Entry(self, textvariable=self.txtvar, width=12, bg="white", fg='#4c4c4c', justify=tk.CENTER)
        timeout_entry.grid(row=2, column=0, padx=6)
        timeout_entry.bind("<Button-1>", clear_timeout)
        timeout_entry.bind("<FocusOut>", restore_timeout)

        main_but_var = tk.IntVar()
        main_but = tk.Checkbutton(self, text='Main Power', width=10, height=1, indicatoron=0, variable=main_but_var,
                                  fg='red', command=self.main_power)
        main_but.grid(row=0, column=0, pady=5)

        tog_but_var = tk.IntVar()
        tog_but = tk.Checkbutton(self, text=self.nick, width=width, height=height, indicatoron=0, variable=tog_but_var,
                                 command=self.SFbutton_pressed)
        tog_but.grid(row=1, column=0)

        # label = tk.Label(self, text=self.nick)
        # label.grid(row=3, column=0)

        self.but_stat = [main_but_var, tog_but_var]

    def main_power(self, txt='MainPower'):

        # power off
        if self.but_stat[0].get() == 0:
            self.allow_to_switch = 0
            self.HW_output.set_state(0, 0)
            if bool(self.HW_output.get_state()[1]):
                self.execute_command(0, 'MainSwitch ShutDown')

        # power on
        elif self.but_stat[0].get() == 1:
            self.allow_to_switch = 1
            self.HW_output.set_state(0, 1)

        if self.switch_type == '': self.switch_type = 'SFButton'
        print([self.nick, self.switch_type, txt, self.HW_output.get_state()[0]])

    def execute_command(self, state, txt=''):

        # On/Off
        if self.allow_to_switch == 1:
            if state == 1:  # Switch on
                if not bool(self.HW_output.get_state()[1]):
                    self.HW_output.set_state(1, 1)
                    self.but_stat[1].set(1)
            elif state == 0:  # Swotch off
                if bool(self.HW_output.get_state()[1]):
                    self.HW_output.set_state(1, 0)
                    self.but_stat[1].set(0)

        # State = Power Disable
        elif self.allow_to_switch == 0:
            if bool(self.HW_output.get_state()[1]):  # Toggle button is On
                self.HW_output.set_state(1, 0)
                self.but_stat[1].set(0)
            elif not bool(self.HW_output.get_state()[1]):
                self.but_stat[1].set(0)

        print([self.nick, self.switch_type, 'ToggleButton', self.HW_output.get_state()[1], txt])

    def run_schedule(self):

        self.SchRun.run_schedule()
        sched_status = self.SchRun.get_status()

        # sched_status[0][0] is switch on/off sched_status[0][1] is task number
        # if status equal to On or Off and task state wasn't disabled

        if not sched_status[0][0] == -1 and self.task_state[sched_status[0][1]] == 1:
            if not bool(sched_status[0][0]) == self.get_state()[1]:
                self.sched_switch_command(0, sched_status[0][0])

        self.master.after(1000, self.run_schedule)

    def sched_switch_command(self, i, state):
        # i irrelvant
        self.switch_type = 'Schedule'
        self.execute_command(state)

    def disable_sched_task(self):
        try:  # if there is a schedule
            # if schedule in ON- disable it for next run
            if not self.SchRun.get_status()[0][0] == -1:
                self.task_state[self.SchRun.get_status()[0][1]] = 0
                #   ^^------toggle button
        except AttributeError:
            pass

    def SFbutton_pressed(self):

        self.switch_type = 'SFButton'
        if not self.task_state == []: self.disable_sched_task()

        # if self.but_stat[1].get() == 1 :
        # self.execute_command(1)#, 'AutoOff %s minutes'%self.txtvar.get())
        ##self.after(1000, self.execute_command, 0)
        ##self.counter(datetime.datetime.now()+datetime.timedelta(seconds=int(float(self.txtvar.get()))))

        # elif self.but_stat[1].get() == 0 :
        ##self.txtvar.set(self.init_var)
        # self.execute_command(0)

        try:
            if float(self.txtvar.get()) > 0:
                if self.but_stat[1].get() == 1:
                    self.execute_command(1, 'AutoOff %s minutes' % self.txtvar.get())
                    self.after(int(round(float(self.txtvar.get()) * 1000)), self.execute_command, 0)
                    self.counter(datetime.datetime.now() + datetime.timedelta(seconds=int(float(self.txtvar.get()))))

            elif self.but_stat.get() == 0:
                self.txtvar.set(self.init_var)
                self.execute_command(0)

        except ValueError:
            self.txtvar.set(self.init_var)
            self.execute_command(self.but_stat[1].get())

    def counter(self, time):

        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)

        remain_time = chop_microseconds(time - datetime.datetime.now())

        if remain_time.total_seconds() > 0 and self.but_stat[1].get() == 1:
            self.txtvar.set(str(remain_time))
            self.after(1000, self.counter, time)

        elif remain_time.total_seconds() <= 0:
            self.txtvar.set(self.init_var)

    def HWbutton_pressed(self, sw, state):

        self.switch_type = "HWButton"
        self.but_stat[sw].set(state)

        if sw == 0:  # MainsPower
            self.main_power('MainPower')

        elif sw == 1:  # ToggleButton
            self.execute_command(state)

    def get_state(self):
        return self.HW_output.get_state()


# root = tk.Tk()
# a = MainsButton(root)
# a.grid()
# root.mainloop()

# root = tk.Tk()
# a = UpDownButton(root, hw_out=[4, 27], ip_out='192.168.2.113', nickname="UpDown", hw_in=[22, 21],
#                  sched_vector=[[[2], "22:05:30", "22:07:00"], [[3], "07:51:00",
#                                                                "20:33:00"]])  # , sched_vector_down=[[[1], "11:37:30", "11:38:00"], [[2], "14:26:40","22:03:10"]])
# a.grid()
# root.mainloop()
#
root = tk.Tk()
b = ToggleButton(root, ip_out="192.168.2.113", hw_out=[4],
                 hw_in=[22])  # , sched_vector=[[[3], "14:55:00", "14:55:30"], [[3], "14:56:40", "15:38:00"]])
b.grid()
root.mainloop()

# root = tk.Tk()
# a = LongPressButton(root, remote=1,time='100000')
# a.grid()
# root.mainloop()
button_list = {1: 'UpDownButton', 2: 'ToggleButton', 3: 'MainsButton'}

import datetime
import tkinter
import time


class ScheduledEvents:
    def __init__(self, tasks):
        # self.date_schedule = []
        self.tasks = tasks
        self.result_vector = [0] * len(self.tasks)
        self.temp_result_vector = [0] * len(self.tasks)

        if self.check_integrity_time_table() == 0:
            print("Date integrity- OK")
            self.task_time_status()
        else:
            print("Errors in TimeTable")

    def check_integrity_time_table(self):
        time_err, days_err = 0, 0

        for i in range(len(self.tasks)):
            time1 = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
            time2 = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()

            if not self.tasks[i][0] in range(0, 8):
                print("day of task %d is not valid" % i)
                days_err += 1

            if not time2 > time1:
                print("Time interval of task %d is not valid" % i)
                time_err += 1

        if time_err + days_err == 0:
            return 0  # No Errors
        else:
            return 1  # Errors on TimeTable

    def task_time_status(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days = [2, 3, 4, 5, 6, 7, 1]

        def time_diff(t1):
            t2 = datetime.datetime.now().time()
            today1 = datetime.date.today()
            return datetime.datetime.combine(today1, t1) - datetime.datetime.combine(today1, t2)

        for i in range(len(self.tasks)):
            start_time = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
            stop_time = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()
            if self.tasks[i][0] == days[datetime.date.today().isoweekday() - 1]:
                # print("Task %d starts on %s at %s and stop at %s" % (i, days[self.tasks[i][0]-7], start_time, stop_time))
                if start_time > datetime.datetime.now().time():
                    # print("task %d will start in %s" % (i, time_diff(start_time)))
                    self.result_vector[i] = [0, time_diff(start_time)]
                    pass

                elif (start_time < datetime.datetime.now().time()) and (datetime.datetime.now().time() < stop_time):
                    # print("task %d is On and will stop in %s" % (i, time_diff(stop_time)))
                    self.result_vector[i] = [1, time_diff(stop_time)]

                elif datetime.datetime.now().time() > stop_time:
                    # print("task %d is Off for %s" % (i, time_diff(stop_time)))
                    self.result_vector[i] = [0, time_diff(stop_time)]

            elif self.tasks[i][0] > days[datetime.date.today().isoweekday() - 1]:
                # print("Task %d will start in %d days" % (i, self.tasks[i][0] - days[datetime.date.today().isoweekday() - 1]))
                self.result_vector[i] = [0, time_diff(start_time)] #, datetime.datetime.combine(
                    # datetime.datetime.now().day + (self.tasks[i][0] - days[datetime.date.today().isoweekday() - 1]),
                    # datetime.datetime.strp(self.tasks[i][1], % H: % m: % S)])

            elif self.tasks[i][0] < days[
                    datetime.date.today().isoweekday() - 1]:  # print("Task %d started %d days ago" % (i, days[datetime.date.today().isoweekday() - 1] - self.tasks[i][0]))
                self.result_vector[i] = [0, time_diff(start_time)]

    def get_status(self):
        return self.result_vector

#
# #sched_for_button = [[0, "08:44:00", "09:44:00"], [2, "13:58:40", "14:00:00"], [3, "14:31:00", "14:44:00"],[4, "17:29:00", "17:29:10"], [4, "09:00:00", "16:44:00"], [5, "08:00:00", "09:00:00"]]
# sched_for_button = [[1, "09:40:00", "09:50:10"]]
# # root = tkinter.Tk()
# a = ScheduledEvents(sched_for_button)
# # root.mainloop()
#
#
#
#
#
#
#

# i , itr, tol = 0 , 0 , 30
# t , task = [] , []

# while True:
#     print (">>iteration #",itr)
#     now = datetime.datetime.now().time()
#     for i in range(0,len(task_time)):
#         t.insert(i,(time_diff(datetime.datetime.strptime(task_time[i],"%H:%M:%S").time()).total_seconds()))
#         if t[i]< 0 -tol:
#             print ("\ttask %d accured in past %d seconds ago" %(i,t[i]))
#         elif t[i] >0 +tol:
#             print("\ttask %d will accure in %d seconds " % (i, t[i]))
#         elif t[i] < (tol) and t[i] > (-tol):
#             print("\ttask # %d >>operation: \n\taccured successfully in %s, at diff %d" % (i, str(now), t[i]))
#             actions(i)
#             actions(0)
#
#
#             time.sleep(tol)
#
#     time.sleep(tol)
#     print("~~~~~~~~~~~~~~~~~")
#     itr +=1

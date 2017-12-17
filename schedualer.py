import datetime
import time
import gmailmod


def time_diff(t1):
    t2 = datetime.datetime.now().time()
    today = datetime.date.today()
    return datetime.datetime.combine(today, t1)-datetime.datetime.combine(today, t2)

def actions(k):
    if k == 0:
        gmailmod.sendmail("guydvir2@gmail.com" , "Automated email" , "Hello there %s" %str(now))
    elif k==1:
        print("action2")
    elif k==2:
        print("action3")

task_time = ["08:44:00","13:58:40", "14:31:00", "17:00:00"]
i , itr, tol = 0 , 0 , 30
t , task = [] , []

while True:
    print (">>iteration #",itr)
    now = datetime.datetime.now().time()
    for i in range(0,len(task_time)):
        t.insert(i,(time_diff(datetime.datetime.strptime(task_time[i],"%H:%M:%S").time()).total_seconds()))
        if t[i]< 0 -tol:
            print ("\ttask %d accured in past %d seconds ago" %(i,t[i]))
        elif t[i] >0 +tol:
            print("\ttask %d will accure in %d seconds " % (i, t[i]))
        elif t[i] < (tol) and t[i] > (-tol):
            print("\ttask # %d >>operation: \n\taccured successfully in %s, at diff %d" % (i, str(now), t[i]))
            actions(i)
            actions(0)


            time.sleep(tol)

    time.sleep(tol)
    print("~~~~~~~~~~~~~~~~~")
    itr +=1



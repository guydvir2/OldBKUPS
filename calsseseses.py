class A:
    class C:
        def __init__(self, master, v, i):
            self.x = v + i
            print("C variable was created")
            print("in C Class, and my master is:", master.firstname)
            self.CB = B(master) # create B Class var and passing A Class as Master

        def print_c(self):
            print("running function print_c inside Class C", self.x)

    def __init__(self, first, last, birthday, *args):
        print("A class variable was created")
        self.firstname = first
        self.lastname = last
        self.bday = birthday
        #self.email()
        self.c1 = self.C(self, *args) #Create C Class variable

    def email(self):
        def doit(arg1):
            print("this is value inside", arg1)

        print(self.firstname + '.' + self.lastname + '@' + 'gmail.com')
        doit(self.bday)
        print("this is value outside", self.bday)


class B:
    def __init__(self, master):
        print("B Class created, inheret A Class parameters via a C Class:", master.firstname, master.lastname)



#Creating variables :

a1 = A("Jhon", 'Doe', '13/12/1985', 11, 12) # create a1- an A Class variable with parameters
print("My email value from A Class:", a1.email()) # calling methon "email" belongs to a1
a1.c1.print_c() # calling c1 variable, part of a1 variable declared earlier


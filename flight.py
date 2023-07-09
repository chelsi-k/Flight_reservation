import mysql.connector
from tabulate import tabulate
import csv
import sys
conn=mysql.connector.connect(host='localhost',user='root',password='aditi',db='Flight_Reservation')
c1=conn.cursor()

class account():
    def home(self):
        print("""*******************************\n*******************************\n\tWELCOME TO \n  FLIGHT RESERVATION SYSTEM
            \n\tAIRJET SOFTWARE\n*******************************\n*******************************""")
        self.time()
        print("""\n MAIN MENU
        Press 1 to Login
        Press 2 to Create Account
        Press 3 to Delete Account
        Press 4 to Exit \n
          """)
        self.choice()
       
    def login(self):
        c1.execute("select * from acc_details")
        self.u=str(input("Enter Username: "))
        data=c1.fetchall()
        p=0
        for i in data:
            if self.u==i[1]:
                v=1
                p+=1
                break
            else:
                v=0
                p+=1
        y='True'
        if v==1:
            self.pw=input("Enter Password: ")
            while y=='True':
                if self.pw==data[p-1][2]:
                    self.pno=data[p-1][3]
                    print("==========LOGIN SUCCESSFULL==========")
                    print("\nWELCOME",self.u,"!")
                    y='False'
                else:
                    print('INCORRECT PASSWORD, PLEASE TRY AGAIN')
                    self.pw=input("Enter Password: ")
        elif v==0:
            print('INVALID USERNAME, PLEASE TRY AGAIN')
            self.login()

    def create(self):
        self.u=str(input("Create Username: (not more than 20 characters)"))
        c1.execute("select * from acc_details")
        data=c1.fetchall()
        p=0
        for i in data:
            if self.u==i[1]:
                v=1
                p+=1
                break
            else:
                v=0
                p+=1
        if v==0:
            self.pw=str(input("Create Password: "))
            self.name=input('Enter your Name(as per your passport):')
            self.pno=int(input("Enter Phone Number: "))
            val=(self.name,self.u,self.pw,self.pno)
            cmd='insert into acc_details values(%s,%s,%s,%s)'
            c1.execute(cmd,val)
            conn.commit()
            print("\n==========ACCOUNT CREATED SUCCESSFULLY==========\n")
        elif v==1:
            print("THIS USERNAME IS ALREADY TAKEN, PLEASE TRY AGAIN")
            self.create()
       
    def delete(self):
        self.u=str(input("Enter Username: "))
        y='True'
        c1.execute("select * from acc_details")
        data=c1.fetchall()
        p=0
        for i in data:
            if self.u==i[1]:
                v=1
                p+=1
                break
            else:
                v=0
                p+=1
        y='True'
        if v==1:
            self.pw=input("Enter Password: ")
            while y=='True':
                if self.pw==data[p-1][2]:
                    val=(self.u)
                    #cmd="delete from acc_details where Username="+str(self.u)
                    #c1.execute(cmd)
                    cmd=("delete from acc_details where Username='%s'"%val)
                    c1.execute(cmd)
                    conn.commit()
                    print("\n==========ACCOUNT DELETED SUCCESSFULLY==========\n")
                    y='False'
                else:
                    print('INCORRECT PASSWORD, PLEASE TRY AGAIN')
                    self.pw=input("Enter Password: ")
        elif v==0:
            print('INVALID USERNAME, PLEASE TRY AGAIN')
            self.delete()
              
    def choice(self):
        self.ch=int(input("Enter your choice:"))
        if self.ch==1:
            self.login()
        elif self.ch==2:
            self.create()
        elif self.ch==3:
            self.delete()
            c=input("Do you wish to continue?(y/n)")
            if c.lower()=='y':
                self.home()
            elif c.lower()=='n':
                self.exit()
        elif self.ch==4:
            self.exit()
        else:
            print("Wrong Input")
            self.choice()
        self.main()

    def main(self):
        print("\n===================================\n==========AIRJET SOFTWARE==========\n===================================")
        self.time()
        print('''\nPlease choose the option that you are here for today!\n\tMain Menu
          1.Book Tickets
          2.Change Registration
          3.Cancel Ticket
          4.My Ticket
          5.Exit
          ''')
        self.che()

    def flight(self):
        print('\nAIRJET offers the following flights: ')
        with open('flight.csv','r') as f:
            csvFile = csv.reader(f)  
            a=[]
            for x in csvFile:
                print(x)
                a.append(x)
            self.from1=input("\nFrom:")
            self.to=input("Destination:")
            v=0
            p=0
            for i in a:
                if self.from1==i[1]:
                    v=1
                    p+=1
                    if self.to==i[2]:
                        self.fno=i[0]
                        v=2
                        p+=1
                        break
                    else:
                        v=0
                        p+=1
                       
                else:
                    v=0
                    p+=1
                    continue
            y='true'
            while y=='true':
                if v==2:
                    y='false'
                    break
                elif v==0:
                    print("Sorry, Airjet doesn't offer a flight from",self.from1,"to",self.to)
                    self.flight()
       
    def book(self):
        self.flight()
        self.date=input("\nEnter date of departure(yyyy-mm-dd): ")
        self.na=int(input("\nEnter number of adult passengers: "))
        self.nc=int(input("Enter number of child passengers: "))
        for i in range(1,self.na+self.nc+1):
            print('')
            self.name=str(input("Enter name of passenger: "))
            self.passportno=input("Enter passport number: ")
            self.seating()
            print('')
            choice2=input("Do you want to add meal to your ticket?(y/n) ")
            if choice2=='y':
                self.meal=input("\nEnter V for VEGETARIAN or NV for NON-VEG meal:  ")
            elif choice2=='n':
                self.meal='-'
            val=[self.passportno,self.name,self.fno,self.date,self.from1,self.to,self.seat,self.seattype,self.meal,self.pno]
            cmd="insert into customerbookings values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            c1.execute(cmd,val)
            conn.commit()
        print("""\nPrice:
        Adult(Age 11+): 1000Dhs/-
        Child(Age 2-11): 700Dhs/-
        Ticket is free for infants(children under the age of 2 years)""")
        print('')
        if self.na==0:
            pass
        elif self.na==1:
            print('Cost for 1 adult is 1000Dhs/-')
        else:
            print('Cost for',self.na,'adults is',1000*(self.na),'Dhs/-')
        if self.nc==0:
            pass
        elif self.nc==1:
            print('Cost for 1 child is 700Dhs/-')
        else:
            print('Cost for',self.nc,'children is',700*(self.nc),'Dhs/-')
        print('TOTAL=',1000*(self.na)+700*(self.nc),'Dhs/-')
        print('\nPAYMENT:')
        self.pay()

    def pay(self):
        cardno=str(input("Enter your 16 digit card number:  "))
        if len(cardno)==16:
            choice3=input('Enter y if the card number you entered is correct, else enter n(y/n)')
            if choice3=='y':
                cvv=int(input("\nEnter CVV number:"))
                print('\n==========PAYMENT SUCCESSFUL==========')
            elif choice3=='n':
                self.pay()
            else:
                print('Invalid input')
                self.pay()
        else:
            print("THE CARD NUMBER YOU ENTERED DOES NOT EXIST, PLEASE TRY AGAIN")
            self.pay()
        self.chhh()

    def seating(self):
        self.seattype=input("""\nChoose your Seat Type:\n\nEconomy \t(Enter E)\nFirst Class \t(Enter F)\nBusiness Class  (Enter B)""")
        if self.seattype.upper()=='F':
            val=(self.fno,self.date)
            cmd=("select Seat_Number from customerbookings where Flight_Number=%s and Date=%s and Class='F'")
            c1.execute(cmd,val)
            data=c1.fetchall()
            s=[]
            for i in data:
                s.append(i)
                continue
            if len(s)==0:
                pass
            else:
                print("\nThe following seats are taken:")
                print(s)
            self.seatno=int(input("\nEnter Seat Number(1-5):"))

        elif self.seattype.upper()=='B':
            val=(self.fno,self.date)
            cmd=("select Seat_Number from customerbookings where Flight_Number=%s and Date=%s and Class='B'")
            c1.execute(cmd,val)
            data=c1.fetchall()
            s=[]
            for i in data:
                s.append(i)
                continue
            if len(s)==0:
                pass
            else:
                print("\nThe following seats are taken:")
                print(s)
            self.seatno=int(input("\nEnter Seat Number(6-10):"))
            
        elif self.seattype.upper()=='E':
            val=(self.fno,self.date)
            cmd=("select Seat_Number from customerbookings where Flight_Number=%s and Date=%s and Class='E'")
            c1.execute(cmd,val)
            data=c1.fetchall()
            s=[]
            for i in data:
                s.append(i)
                continue
            if len(s)==0:
                pass
            else:
                print("\nThe following seats are taken:")
                print(s)
            self.seatno=int(input("\nEnter Seat Number(11-30):"))
            
        else:
            print("\nWrong Input")
            self.seating()
        self.row=input("Select Row (A/B/C/D/E/F):")
        self.seat=str(self.seatno)+self.row
        print('\nName:',self.name)
        print('Passport number:',self.passportno)
        print('Seat:',self.seat)
        choice1=input("\nDo you want to change seats? (y/n)")
        if choice1.lower()=='y':
            self.seating()
        elif choice1.lower()=='n':
            pass
               
    def update(self):
        print("""\n\tUPDATE
            1. Flight
            2. Date of Flying
            3. Seat
            4. Meal""")
        u=int(input("Enter what you want to change:  "))
        if u==1:
            for i in range(0,len(self.t)):
                self.name=self.t[i][1]
                print('\n',self.name.upper())
                self.flight()
                values=(self.from1,self.name)
                command="update customerbookings set Departure=%s where Passenger_Name=%s"
                c1.execute(command,values)
                conn.commit()
                val=(self.to,self.name)
                command="update customerbookings set Arrival=%s where Passenger_Name=%s"
                c1.execute(command,val)
                conn.commit()
                vals=(self.fno,self.name)
                command="update customerbookings set Flight_Number=%s where Passenger_Name=%s"
                c1.execute(command,vals)
                conn.commit()
           
        elif u==2:
            self.newdate=input("Enter new date of flying(yyyy-mm-dd)")
            values=(self.newdate,self.pno)
            command="update customerbookings set Date=%s where PhoneNo=%s"
            c1.execute(command,values)
            conn.commit()
           
        elif u==3:
            for i in range(0,len(self.t)):
                self.fno=self.t[i][2]
                self.name=self.t[i][1]
                self.date=self.t[i][3]
                print('\n',self.name.upper())
                self.passportno=self.t[i][0]
                self.seating()
                val=(self.seat,self.name)
                cmd="update customerbookings set Seat_Number=%s where Passenger_Name=%s"
                vals=(self.seattype,self.name)
                #print(self.seattype)
                cmd="update customerbookings set Class=%s where Passenger_Name=%s"
                c1.execute(cmd,vals)
                conn.commit()
               
        elif u==4:
            for i in range(0,len(self.t)):
                self.name=self.t[i][1]
                print('\n',self.name.upper())
                choice2=input("Do you want to add meal to your ticket?(y/n)")
                if choice2.lower()=='y':
                    self.meal=input("Enter V for VEGETARIAN or NV for NON-VEG meal:  ")
                elif choice2.lower()=='n':
                    self.meal='-'
                val=(self.meal,self.name)
                cmd="update customerbookings set Meal=%s where Passenger_Name=%s"
                c1.execute(cmd,val)
                conn.commit()
        print("==========BOOKING UPDATED SUCCESSFULLY==========")
        self.cont()
               
    def cancel(self):
        self.pno=int(input("Enter your registered phone number:  "))
        cmd="select Passport_Number,Passenger_Name,Flight_Number,Date,Departure,Arrival,Seat_Number,Class,Meal from customerbookings where PhoneNo="+str(self.pno)
        c1.execute(cmd,self.pno)
        c=[]
        h=['Passport_Number','Passenger_Name','Flight_Number','Date','Departure','Arrival','Seat_Number','Class','Meal']
        x=c1.fetchall()
        print(tabulate(x,headers=h,tablefmt='fancy_grid'))
        for i in x:
            c.append(i)
            continue
        if len(c)==0:
            print("YOU DO NOT HAVE ANY BOOKINGS")
            pass
        else:
            chh=input("Are you sure you want to cancel your booking?(y/n)")
            if chh.lower()=='y':
                val=(self.pno)
                #cmd="delete from customerbookings where PhoneNo="+str(self.pno)
                cmd=("delete from customerbookings where PhoneNo=%s"%val)
                c1.execute(cmd,val)
                conn.commit()
                print("==========BOOKING DELETED SUCCESSFULLY==========")
            elif chh.lower()=='n':
                self.main()
        self.chhh()

    def ticket(self):
        self.pno=int(input("Enter your registered phone number:  "))
        cmd="select Passport_Number,Passenger_Name,Flight_Number,Date,Departure,Arrival,Seat_Number,Class,Meal from customerbookings where PhoneNo="+str(self.pno)
        c1.execute(cmd,self.pno)
        print("\nYour Booking:\n")
        t=[]
        h=['Passport_Number','Passenger_Name','Flight_Number','Date','Departure','Arrival','Seat_Number','Class','Meal']
        x=c1.fetchall()
        print(tabulate(x,headers=h,tablefmt='fancy_grid'))
        for i in x:
            t.append(i)
            continue
        if len(t)==0:
            print("YOU HAVE NO BOOKINGS")
            pass
        else:
            pass
       
    def che(self):
        choice=int(input("Enter your choice:"))
        if choice==1:
            self.book()
        elif choice==2:
            self.change()
        elif choice==3:
            self.cancel()  
        elif choice==4:
            self.ticket()    
        elif choice==5:
            self.exit()
        else:
            print("Wrong Input")
            self.che()
        self.chhh()
      
a=account()
a.home()

from random import randint
from datetime import date

import pymysql
conn=pymysql.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="karthik_test"
)
var=0
cursor=conn.cursor()
def authority_login():# AUTHORITY LOGIN TO ENTER AND DELETE BUSES DATA
    global var
    true_pin="1234@56"
    pin=input("Enter pin * ")
    if pin==true_pin:
        inp =input("enter password to EREASE the previous data  OR  UPDATE bus details * ").upper()

        if inp=="GPREC@EREASE":
            display()
            print(("CLICK 134 TO ONLY EREASE THE PASSENGER PREVIOUS DATA IF THE BUSNO , STARTING AND ENDING POINTS ARE SAME "))
            print("CLICK 228 TO EREASE ALL DATA REFERING TO BUS , POINTS , PASSENGERS ")

            var=int(input())
            if var==134:
                cursor.execute("truncate  data")
                return
            if var==228:
                cursor.execute("truncate data")
                cursor.execute("truncate points")
                cursor.execute("truncate authority")
                exit ()
        if inp=="GPREC@UPDATE":
           date=input("Enter date of journey  YYYY-MM-DD * ")
           bus_no=input("Enter bus number * ").upper()
           starting_station=input("Enter starting station * ").upper()

           toa=input("Enter depature time of starting station  __:__ AM or PM * ").upper()
           ending_station=input("Enter ending station * ").upper()
           try:
              seats=int(input("Enter number of seats * "))
           except ValueError:
               print("INVALID NUMBER  \n SECURITY THREAT<<<<<<< LOGIN ONCE MORE ")
               return
           cursor.execute("insert into points (sp,ep,bus_no,seats,date_info)values(%s,%s,%s,%s,%s)",(starting_station,ending_station,bus_no,seats,date))
           cursor.execute("insert into authority(stage_name,time_of_arrival,price) values(%s,%s,%s)",(starting_station,toa,"0"))
           try:
              inp = int(input("Enter no of stages * "))
           except ValueError:
               print("INVALID NUMBER  \nSECURITY THREAT<<<<<<< LOGIN ONCE MORE ")
               return
           for i in range(0, inp):
            stage_name = input(f"Enter stage {i + 1} * ")
            toa = input("Enter time of arrival  __:__ AM or PM * ")
            try:
                price = int(input("Enter price * "))
            except ValueError:
                print("invalid price \nsecurity threat login once more")
                return
            cursor.execute("insert into authority (stage_name,time_of_arrival,price)values(%s,%s,%s)",
                           (stage_name, toa, price))
        else:
            print("invalid password ")
            return
        conn.commit()
        display()
        return
    else:
                print("INVALID PIN !!!")
                print("BLOCKED !!!!!  LOGIN AFTER 6 HOURS !!!!!")
                exit()

def display(): #DISPLAY BOARD FUNCTION
        cursor.execute("select*from points")
        val=cursor.fetchall()
        for i in val:

          print(f"******--WELCOME TO GPREC TRAVELS FROM [{i[0]} TO {i[1]}]--****** ")
          print(f"BUS NO {i[2]} :  NO OF SEATS {i[3]}  JOURNEY DATE : {i[4]}")
def view_stopings():
    print("")
    cursor.execute("select stage,stage_name,time_of_arrival from authority ")
    data=cursor.fetchall()
    for i in data:
        print(f"stage {i[0]} : {i[1]} <-----------> time of arrival : {i[2]} ")
        print()
def payment(st,ed):# PAYMENT FUNCTION
    if st==ed:
        print("TWO STATIONS ARE SAME !!!!")
        return 3
    cursor.execute("select price from authority where stage_name in (%s , %s)",(st,ed))
    pay=cursor.fetchall()
    price=int(pay[1][0])-int(pay[0][0])
    print(f"price {price}")
    try :
        pay_con=int(input("CLICK 8 TO PAY : "))
    except ValueError :
        print("INVALID OPTION ")
        return 0
    if pay_con==8:
        i=0
        while i!=3:
          try:
              amount=int(input(f"please pay {price} : "))
          except ValueError:
              print("INVALID PRICE ")
              i+=1
              continue
          if amount==price:
              print("PAYMENT SUCCESSFUL")
              break
          else:
              i=i+1
        if i==3:
            return i
def reservation(bs, name, age, sex, mobile_no, st, ed):# ENTERING PASSENGER DETAILS INTO DATA BASE
    sql = ("insert into data(passenger_name, age,sex, seat_no,mobile_no,starting_point, ending_point,reservation_no)"
           "values(%s,%s,%s,%s,%s,%s,%s,%s)")
    rno = randint(1000, 2000)
    values = (name, age, sex, bs, mobile_no, st, ed, rno)
    cursor.execute(sql, values)
    conn.commit()
    viewreservation(rno)
    print(" ******** THANK YOU ******** ")

def viewreservation(rno):# FUNCTION TO CHECK THE ENTERED SEAT NO IS VALID OR NOT
    cursor.execute("select * from data where  reservation_no= %s ", rno)
    op = cursor.fetchone()
    print(f"reservation_id : {op[0]} ---- name : {op[1]}\nage : {op[2]} ---- sex : {op[3]}\nseat_no : {op[4]} ---- mobile_no : {op[5]}\nstp : {op[6]} ---- ep {op[7]}\nreservation_no : {op[8]}")
def bookingseats(i,nos):
    k=0
    if nos==1:
      while k!=3:
        try :
          bs = int(input("Enter seat number to book : "))
          break
        except ValueError:
          print("invalid  seat_no !!!!")
          k+=1
          if k==3:
              return 0
      cursor.execute("select seat_no from data where seat_no=%s", (bs,))
      sn=cursor.fetchone()
      sn=int(sn[0]) if sn and sn[0] is not None else 0
      if sn==bs  :
        print(f"seat {bs} is booked by others")
        print("enter seat no that is not booked by others")
        return bookingseats(i,nos)
      cursor.execute("select seats from points ")
      max_sno=cursor.fetchone()
      max_sno=int(max_sno[0])
      if bs>max_sno or bs<=0:
        print(f"Enter seat number greather than 0 and less than {max_sno}")
        return bookingseats(i,nos)
    if nos>1:
        while k!=3:
          try :
              bs = int(input(f"Enter person {i} seat number : "))
              break
          except ValueError:
            print("Invalid _number !!!!")
            k+=1
            if k==3:
                return 0
        cursor.execute("select seat_no from data where seat_no=%s", (bs,))
        sn = cursor.fetchone()
        sn = int(sn[0]) if sn and sn[0] is not None else 0
        if sn == bs:
            print(f"seat {bs} is booked by others")
            print("enter seat no that is not booked by others")
            return bookingseats(i,nos)
        cursor.execute("select seats from points ")
        max_sno = cursor.fetchone()
        max_sno = int(max_sno[0])
        if bs > max_sno or bs <= 0:
            print(f"Enter seat number greather than 0 and less than {max_sno}")
            return bookingseats(nos,nos)
    return bs
def view_seats():# FUNCTION TO VIEW SEATS
    cursor.execute("select seats from points")
    seats=cursor.fetchone()
    cursor.execute("select seat_no from data")
    seat_no=cursor.fetchall()
    seats=int(seats[0])

    list=[]
    for j in seat_no:
        list.append(int(j[0]))

    for i in range(1,seats+1):
            if i in list:
                b="BKD"
                cursor.execute("select sex from data where seat_no=%s",(i))
                sex = cursor.fetchone()
                if sex[0]=="F":

                    print("B(F)",end=' ')
                else:
                    print(b.ljust(5), end=' ')
            else:
                print(str(i).ljust(5),end=' ')
            if (i) % 2 == 0:
                print(end='     ')
            if (i) % 4 == 0:
                print("")

    print("")
def bookseats():# FUNCTION TO BOOK SEATS
    nos=0
    cursor.execute("select max(passenger_id) from data")
    max_sno = cursor.fetchone()
    cursor.execute("select seats from points ")
    no_of_seats=cursor.fetchone()
    max_sno=int(max_sno[0]) if max_sno[0] is not None else 0
    no_of_seats=int(no_of_seats[0]) if no_of_seats and no_of_seats[0] is not None else 0
    try :
        nos=int(input("Enter number of seats to be book : "))
    except ValueError:
        print("invald number !!!!")
        bookseats()
    if nos <= no_of_seats - max_sno:
        if nos==1:
            bs=bookingseats(nos,nos)
            if bs==0:
                return
            name = input("Enter name : ").upper()
            age=mobile_no=sex=None
            age_con=sex_con=mobile_no_con=None
            for k in range(0,3):
               try :
                   if age_con!=0:
                      age = int(input("Enter age : "))
                      age_con=0
               except ValueError:
                   print("Invalid age !!!")
                   age_con = 1
                   continue
               try :
                   if sex_con!=0:
                      sex = input("Enter (M if male)||(F if female) : ").upper()
                      sex_con=0
               except ValueError:
                   sex_con=1
                   continue
               try :
                   if mobile_no_con!=0:
                      mobile_no = int(input("Enter mobile no : "))
                      mobile_no_con=0
               except ValueError:
                   mobile_no=1
                   continue
            st="randam"
            ed="random"
            var=0
            stp=None
            edp='random'
            while stp!=edp:
              st = input("Enter starting point : ")
              cursor.execute("select stage_name from authority where stage_name = %s",(st,))
              spr=cursor.fetchone()
              if spr==None:
                print("starting point not matched !!!! ")
                continue
              else:
                  stp="true"

              while var!=3:
                ed = input("Enter ending point : ")
                cursor.execute("select stage_name from authority where stage_name =%s",(ed,))
                epr=cursor.fetchone()
                if epr==None:
                    print("ending point not matched !!!! ")
                    var+=1
                else:
                    edp="true"
                    break
              if stp==edp:
                  break
            i=payment(st,ed)
            if i==3 or i==0:
                return
            reservation(bs, name, age, sex, mobile_no, st, ed)

        else :
          if nos>1:
            age = sex = mobile_no = None
            for i in range(0,nos):
              bs = bookingseats(i+1,nos)
              if bs==0:
                  return
              name = input(f"Enter person {i+1} name : ").upper()
              age = mobile_no = sex = None
              age_con = sex_con = mobile_no_con = None
              for k in range(0, 3):
                  try:
                      if age_con != 0:
                          age = int(input("Enter age : "))
                          age_con = 0
                  except ValueError:
                      print("Invalid age !!!")
                      age_con = 1
                      continue
                  try:
                      if sex_con != 0:
                          sex = input("Enter (M if male)||(F if female) : ").upper()
                          sex_con = 0
                  except ValueError:
                      sex_con = 1
                      continue
                  try:
                      if mobile_no_con != 0:
                          mobile_no = int(input("Enter mobile no : "))
                          mobile_no_con = 0
                  except ValueError:
                      mobile_no = 1
                      continue
              st = "randam"
              ed = "random"
              stp=None
              edp="random"
              var = 0
              while stp!=edp:
                st = input("Enter starting point : ")
                cursor.execute("select stage_name from authority where stage_name = %s", (st,))
                spr = cursor.fetchone()
                if spr == None:
                    print("starting point not matched !!!! ")
                    continue
                else:
                    stp = "true"

                edp=None
                while var != 3:
                    ed = input("Enter ending point : ")
                    cursor.execute("select stage_name from authority where stage_name =%s", (ed,))
                    epr = cursor.fetchone()
                    if epr == None:
                        print("ending point not matched !!!! ")
                        var += 1
                    else:
                        edp = "true"
                        break
                if var==3:
                    return
                if stp == edp:
                    break

              i = payment(st, ed)
              if i == 3 or i==0:
                   return
              reservation(bs, name, age, sex, mobile_no, st, ed)
# CHECKING IF THE BUSES ARE AVAILABLE OR NOT
inp=0
cursor.execute("select bus_no from points ")
check=cursor.fetchone()
if check  is None or check[0] is None:
    print("NO BUSES AVAILABLE")
    i=0
    while i!=1:
      secret_pin =input("")
      if secret_pin=="@gprec.authority":
        authority_login()
        i=1
      else:
          print("NO BUSES AVAILABLE")
# DISPLAY DETATAILS ABOUT BUS
display()
while inp!=None:
    #CHOOSING OPTIONS
  inp=input("TO VIEW SEATS('CLICK 1')<->TO VIEW STOPINGS('CLICK 2')<->TO BOOK SEATS('CLICK 3')<->TO VIEW RESERVATION('CLICK 4') : ")
  if inp=='1':
    view_seats()
  if inp=='2':
      view_stopings()
  if inp=='3':
    bookseats()
  if inp=='4':
    try :
        reserve_no=int(input("Enter reservation number : "))
    except ValueError:
        print("INVALID RESERVATION NUMBER !!!!!")
    if cursor.execute("select reservation_no from data where reservation_no=%s",reserve_no):
        viewreservation(reserve_no)
    else:
      continue
  else:# IF INPUT IS THE AUTHORITY PASSWORD
      if inp=="@gprec.authority":
          authority_login()
      else:#  INVALID OPTION HANDLING
          if inp!="1" and inp!='2'and inp!='3' and  inp!='4':
               print("INVALIDE OPTION !!!!")

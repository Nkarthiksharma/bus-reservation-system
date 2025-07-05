import pymysql
from random import randint
conn=pymysql.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="bus"
)
cursor=conn.cursor()
def authoritylogin():
    try:
        ino=int(input("Enter 1 to insert bus ---- enter 2 to erease bus data : "))
    except ValueError:
        print("error login  once more")
        return
    if ino==1:
        date = input("Enter date of journey  DD-MM-YYYY * ")
        i=0
        while i!=3:
          id=input("Enter bus name (NO WHITE SPACES ARE ALLOWED) * ").strip()
          cursor.execute("select bus_info from authority where bus_info=%s", (id,))
          inp=cursor.fetchone()
          if inp==None:
              break
          if inp[0]!=None:
            print("bus name already exits please enter valid bus number")
            i+=1
        if i==3:
             print("login one more")
        bus_no = input("Enter bus number * ").upper()
        cursor.execute("select bus_info from authority where bus_info=%s",(id,))
        starting_station = input("Enter starting station * ").upper()

        toa = input("Enter depature time of starting station  __:__ AM or PM * ").upper()
        ending_station = input("Enter ending station * ").upper()
        try:
            seats = int(input("Enter number of seats * "))
        except ValueError:
            print("INVALID NUMBER  \n SECURITY THREAT<<<<<<< LOGIN ONCE MORE ")
            return
        cursor.execute("insert into authority  (bus_info,bus_no,starting_point,ending_point,date_info,seats)values(%s,%s,%s,%s,%s,%s)",(id,bus_no,starting_station, ending_station,  date, seats))
        cursor.execute(f""" create table if not exists {id} (
                             stage_id int primary key auto_increment,
                              stage_name varchar(30),
                              time varchar(30),
                                price int)""")
        cursor.execute(f"insert into {id} (stage_name,time,price) values(%s,%s,%s)",
                       (starting_station, toa, "0"))
        try:
            inp = int(input("Enter no of stages * "))
        except ValueError:
            print("INVALID NUMBER  \nSECURITY THREAT<<<<<<< LOGIN ONCE MORE ")
            return
        for i in range(0, inp):
            stage_name = input(f"Enter stage {i + 1} * ").upper()
            toa = input("Enter time of arrival  __:__ AM or PM * ").upper()
            try:
                price = int(input("Enter price * "))
            except ValueError:
                print("invalid price \nsecurity threat login once more")
                return
            cursor.execute(f"insert into {id} (stage_name,time,price)values(%s,%s,%s)",
                           (stage_name, toa, price))
        cursor.execute(f""" create table if not exists {bus_no}(
                                     passenger_id int primary key AUTO_INCREMENT,
                                     passenger_name varchar(30) ,
                                     age int ,
                                    sex varchar(2),
                                    seat_no int ,
                                     mobile_no varchar(10) ,
                                       starting_point varchar(30) ,
                                     ending_point varchar(30) ,
                                   reservation_no int )""")
        print("SUCCESSFULLY INSERTED")
    elif ino==2:
            er=input("enter bus _no to erease ").strip()
            cursor.execute("select bus_no from authority where bus_no=%s",(er,))
            erc=cursor.fetchone()
            if erc==None:
                print("the bus not exists")
                return
            e=int(input("click 224 to erease only passenger data if the starting and ending points are same \n232 to erease the bus "))
            if e ==224:
                cursor.execute(f"truncate {er}")
                print("successfully ereased")
            if e==232:
                cursor.execute(f"drop table {er}")
                cursor.execute(f"select bus_info from authority where bus_no=%s",(er,))
                i=cursor.fetchone()
                cursor.execute(f"drop table {i[0]}")
                cursor.execute("delete from authority where bus_no=%s",(er,))
                print("successfully ereased")
    else:
        print("invalid password ")
        return
    conn.commit()

def payment(st,ed,id):# PAYMENT FUNCTION
    if st==ed:
        print("TWO STATIONS ARE SAME !!!!")
        return 3
    cursor.execute(f"select price from {id} where stage_name in (%s , %s)",(st,ed))
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
def reservation(bs, name, age, sex, mobile_no, st, ed,book):# ENTERING PASSENGER DETAILS INTO DATA BASE
    sql = (f"insert into {book}(passenger_name, age,sex, seat_no,mobile_no,starting_point, ending_point,reservation_no)"
           "values(%s,%s,%s,%s,%s,%s,%s,%s)")
    rno = randint(1000, 2000)
    values = (name, age, sex, bs, mobile_no, st, ed, rno)
    cursor.execute(sql, values)
    conn.commit()
    viewreservation(rno,book)
    print(" ******** THANK YOU ******** ")
def viewreservation(rno,book):# FUNCTION TO CHECK THE ENTERED SEAT NO IS VALID OR NOT
    cursor.execute(f"select * from {book} where  reservation_no= %s ", rno)
    op = cursor.fetchone()
    cursor.execute("select date_info from authority where bus_no=%s",(book,))
    s=cursor.fetchone()
    print(f" bus_no : {book} ---- date {s[0]} ---- reservation_id : {op[0]} ---- name : {op[1]}\nage : {op[2]} ---- sex : {op[3]}\nseat_no : {op[4]} ---- mobile_no : {op[5]}\nstp : {op[6]} ---- ep {op[7]}\nreservation_no : {op[8]}")
def bookingseats (i,nos,book):
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
      cursor.execute(f"select seat_no from {book} where seat_no=%s", (bs,))
      sn=cursor.fetchone()
      sn=int(sn[0]) if sn and sn[0] is not None else 0
      if sn==bs  :
        print(f"seat {bs} is booked by others")
        print("enter seat no that is not booked by others")
        return bookingseats(i,nos,book)
      cursor.execute("select seats from authority where bus_no=%s ",(book,))
      max_sno=cursor.fetchone()
      max_sno=int(max_sno[0])
      if bs>max_sno or bs<=0:
        print(f"Enter seat number greather than 0 and less than {max_sno}")
        return bookingseats(i,nos,book)
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
        cursor.execute(f"select seat_no from {book} where seat_no=%s", (bs,))
        sn = cursor.fetchone()
        sn = int(sn[0]) if sn and sn[0] is not None else 0
        if sn == bs:
            print(f"seat {bs} is booked by others")
            print("enter seat no that is not booked by others")
            return bookingseats(i,nos,book)
        cursor.execute("select seats from authority where bus_no=%s ",(book,))
        max_sno = cursor.fetchone()
        max_sno = int(max_sno[0])
        if bs > max_sno or bs <= 0:
            print(f"Enter seat number greather than 0 and less than {max_sno}")
            return bookingseats(nos,nos,book)
    return bs
def view_seats(book,id):# FUNCTION TO VIEW SEATS
    cursor.execute("select seats from authority where bus_no=%s",(book,))
    seats=cursor.fetchone()
    cursor.execute(f"select seat_no from {book}")
    seat_no=cursor.fetchall()
    seats=int(seats[0])

    list=[]
    for j in seat_no:
        list.append(int(j[0]))

    for i in range(1,seats+1):
            if i in list:
                b=" "
                cursor.execute(f"select sex from {book} where seat_no=%s",(i,))
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
def bookseats(book,id):# FUNCTION TO BOOK SEATS
    nos=0
    cursor.execute(f"select max(passenger_id) from {book}")
    max_sno = cursor.fetchone()
    cursor.execute(f"select seats from authority where bus_no=%s ",(book,))
    no_of_seats=cursor.fetchone()
    max_sno=int(max_sno[0]) if max_sno[0] is not None else 0
    no_of_seats=int(no_of_seats[0]) if no_of_seats and no_of_seats[0] is not None else 0
    try :
        nos=int(input("Enter number of seats to be book : "))
    except ValueError:
        print("invald number !!!!")
        bookseats(book,id)
    if nos <= no_of_seats - max_sno:
        if nos==1:
            bs=bookingseats(nos,nos,book)
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
              cursor.execute(f"select stage_name from {id} where stage_name = %s ",(st,))
              spr=cursor.fetchone()
              cursor.execute(f"select stage_id from {id} where stage_name = %s",(st,))
              stv=cursor.fetchone()
              stv=int(stv[0]) if stv and stv[0] is not None else 0
              if spr==None:
                print("starting point not matched !!!! ")
                continue
              else:
                  stp="true"

              while var!=3:
                ed = input("Enter ending point : ")
                cursor.execute(f"select stage_id,stage_name from {id} where stage_name =%s",(ed,))
                epr=cursor.fetchone()
                cursor.execute( f"select stage_id from {id} where stage_name = %s", (ed,))
                edv = cursor.fetchone()
                edv = int(edv[0]) if edv and edv[0] is not None else 0
                if epr==None or edv<stv:
                    print("ending point not matched !!!! ")
                    var+=1
                else:
                    edp="true"
                    break
              if stp==edp:
                  break
            i=payment(st,ed,id)
            if i==3 or i==0:
                return
            reservation(bs, name, age, sex, mobile_no, st, ed,book)

        else :
          if nos>1:
            age = sex = mobile_no = None
            for i in range(0,nos):
              bs = bookingseats(i+1,nos,book)
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
                cursor.execute(f"select stage_name from {id} where stage_name = %s", (st,))
                spr = cursor.fetchone()
                cursor.execute(f"select stage_id from {id} where stage_name=%s", (st,))
                stv = cursor.fetchone()
                stv = int(stv[0]) if stv and stv[0] is not None else 0
                if spr == None:
                    print("starting point not matched !!!! ")
                    continue
                else:
                    stp = "true"

                edp=None
                while var != 3:
                    ed = input("Enter ending point : ")
                    cursor.execute(f"select stage_name from {id} where stage_name =%s", (ed,))
                    epr = cursor.fetchone()
                    cursor.execute(f"select stage_id from {id} where stage_name=%s", (ed,))
                    edv = cursor.fetchone()
                    edv = int(edv[0]) if edv and edv[0] is not None else 0
                    if epr == None or edv < stv:
                        print("ending point not matched !!!! ")
                        var += 1
                    else:
                        edp = "true"
                        break
                if var==3:
                    return
                if stp == edp:
                    break

              i = payment(st, ed,id)
              if i == 3 or i==0:
                   return
              reservation(bs, name, age, sex, mobile_no, st, ed,book)
def checking(stp,edp,date):
    bid_list=[]
    s=0
    e=0
    cursor.execute("select bus_info from authority where date_info=%s",(date,))
    buses=cursor.fetchall()
    for i in buses:
         # print(i[0])
         bus_ids=i[0]
         cursor.execute(f"select stage_id from {bus_ids} where stage_name = %s ",(stp,))
         stpn=cursor.fetchone()
         if stpn==None:
             continue
         cursor.execute(f"select stage_id from {bus_ids} where stage_name = %s ",(edp,))
         edpn=cursor.fetchone()
         if edpn==None:
             continue
         if stpn and edpn and int(stpn[0])>int(edpn[0]):
             continue
         # print(bus_ids)
         cursor.execute(f"select stage_name from {bus_ids} where stage_name=%s",(stp,))
         checkstp=cursor.fetchone()

         # print(checkstp[0])
         if checkstp and stp==checkstp[0]:
                  # print("Starting point matched")
                  s=1
         cursor.execute(f"select stage_name from {bus_ids} where stage_name=%s", (edp,))
         checkedp = cursor.fetchone()

         if checkedp and edp==checkedp[0]:
                  # print("Ending point matched")
                  e=1
         if s==1 and e==1:
                bid_list.append(i[0])
    if bid_list == []:
        print(f"NO BUSES FOUND ON {date} REGARDING TO YOUR STOPINGS")
        return
    for i in bid_list:
              cursor.execute("select * from authority where bus_info=%s",(i,))
              details=cursor.fetchone()
              cursor.execute(f"select time from {i} where stage_name=%s ",(stp,))
              rstp=cursor.fetchone()
              if rstp==None:
                  continue
              cursor.execute(f"select time from {i} where stage_name=%s ", (edp,))
              redp = cursor.fetchone()
              if redp==None:
                  continue
              print(f"BUS NO : {details[1]} --- STARTING POINT : {details[2]} --- ENDING POINT : {details[3]}")
              print(f"YOUR STARTING POINT : {stp} --- ARRIVAL TIME : {rstp[0]}\nYOUR ENDING POINT : {edp} --- ARRIVAL TIME : {redp[0]}\n")
    inp=0

    while inp!=3:
     try:
        inp=int(input("click 1 to book seats --- click 2 to view seats --- click 3 to exit : "))
     except ValueError:
        print("Invalid number")
        inp=3
     if inp==1:
       book=input("Enter bus number to book seats").upper()
       cursor.execute("select bus_no,bus_info from authority where bus_no=%s",(book,))
       b=cursor.fetchone()
       if b==None:
           print("invalid bus number !!!!")
           return
       if book==b[0]:
         print(b[1])
         bookseats(book,b[1])
     if inp==2:
        book = input("Enter bus number to view seats").upper()
        cursor.execute("select bus_no,bus_info from authority where bus_no=%s", (book,))
        b = cursor.fetchone()
        if b==None:
            print("invalid bus number !!!!")
            return
        b=b[1]
        view_seats(book,b)

print("****    WELCOME TO GPREC TRAVELS    ****")
while(1):
 try :
     user_inp=int(input("my reservation click 1 ---- to see buses click 2 : "))
 except ValueError:
     print("invalid input ")
     continue
 if user_inp==1:
     book=input("Enter bus number : ")
     cursor.execute("select bus_no from authority where bus_no=%s",(book))
     a=cursor.fetchone()
     if a==None:
         print("bus no not matched")
         continue
     else:
         try :
             rno=int(input("Enter reservation number : "))
         except ValueError:
             print("invalid reservation number")
             continue
         cursor.execute(f"select reservation_no from {book} where reservation_no =%s ",(rno,))
         r=cursor.fetchone()
         if r==None:
             print("reservation number not matched ")
             continue
         if r[0]==rno:
            viewreservation(rno,book)
 if user_inp==2:
  starting_point=input("Enter starting point : ").upper()
  if starting_point=="@GPREC.AUTHORITY":
    authoritylogin()
  ending_point=input("Enter endng point : ").upper()
  date=input("Enter date DD-MM-YYYY : ")
  print("")
  checking(starting_point,ending_point,date)

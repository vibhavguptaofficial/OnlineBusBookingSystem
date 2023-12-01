from tkinter import*
import sqlite3
from tkinter.messagebox import *
from datetime import date
con=sqlite3.connect('myDatabase')
cur=con.cursor()

cur.execute('create table if not exists bus(bus_id varchar(5) not null primary key,bus_type varchar(10),capacity int,fair int,op_id varchar(5) not null,route_id varchar(5) not null,foreign key(op_id) references operator(opr_id),foreign key(route_id) references route(r_id))')
cur.execute('create table if not exists operator(opr_id varchar(5) primary key,name varchar(20),address varchar(50),phone char(10),email varchar(30))')
cur.execute('create table if not exists running(b_id varchar(5) ,run_date date,seat_avail int,foreign key(b_id) references bus(bus_id))')
cur.execute('create table if not exists route(r_id varchar(5) not null primary key,s_name varchar(20),s_id varchar(5),e_name varchar(20),e_id varchar(5) )')
cur.execute('create table if not exists booking_history(name varchar(20),gender char(1),no_of_seat int,phone char(10),age int,booking_ref varchar(10) not null primary key,booking_date date,travel_date date,bid varchar(5),foreign key(bid) references bus(bus_id))')

class onlineBusBookingSystem :

    def home(self):
        root = Tk()
        root.title("Home Page")
        root.configure(bg="light sky blue")
        bus = PhotoImage(file='starbus.png')
 
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))
        Label(root, text='\n\n\n\n\n\n',bg="light sky blue").pack()
        Label(root, image=bus,bg="light sky blue").pack()
        Label(root, text='\n\n',bg="light sky blue").pack()
        Label(root, text=" Online Bus Booking System ", font='Arial 20 bold', bg='azure', fg='blue4').pack()
        Label(root, text="\nName: VIBHAV GUPTA", font='Arial 16 bold', bg="light sky blue", fg='blue').pack()
        Label(root, text="\nEnrollment No. : 221B438", font='Arial 16 bold', bg="light sky blue", fg='blue').pack()
        Label(root, text="\nMobile : 7985443438\n", font='Arial 16 bold', bg="light sky blue", fg='blue').pack()
        Label(root, text="Submitted to : Dr. Mahesh Kumar Sir", font='Arial 15 bold', bg='azure', fg='blue4').pack()
        Label(root, text='\n',bg="light sky blue").pack()
        Label(root, text=" Project Based Learning ", font='Arial 15 bold', bg="blue4", fg='azure').pack()

        def home_to_main(event):
            root.destroy()
            self.main()

        root.bind("<KeyPress>", home_to_main)
        root.mainloop()
        
    def main(self):
        root = Tk()
        root.title("Main Page")
        root.configure(bg="light sky blue")

        bus = PhotoImage(file='starbus.png')
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))
        Label(root, text='\n\n\n\n',bg="light sky blue").grid(row=0, column=0)
        Label(root, image=bus,bg="light sky blue").grid(row=1, column=1, columnspan=12, padx=w // 2.5)
        Label(root, text=" Online Bus Booking System ", font='Arial 20 bold', bg='azure', fg='blue4').grid(row=2, column=2, columnspan=9, padx=w // 2.5)
        def main_to_seatBooking():
            root.destroy()
            self.seatBooking()

        def main_to_checkBooking():
            root.destroy()
            self.checkBooking()

        def main_to_addBusDetails():
            root.destroy()
            self.addBusDetails()

        Label(root, text='\n\n\n\n\n\n',bg="light sky blue").grid(row=3, column=4)
        Button(root, text='Seat Booking', font='Arial 14 bold', bg='blue', fg='snow',command=main_to_seatBooking).grid(row=4, column=4)
        Label(root, text='\n\n\n\n\n\n',bg="light sky blue").grid(row=3, column=6)
        Button(root, text='Check Booked Seat', font='Arial 14 bold', bg='blue', fg='snow',command=main_to_checkBooking).grid(row=4, column=6)
        Label(root, text='\n\n\n\n\n\n',bg="light sky blue").grid(row=3, column=8)
        Button(root, text='Add Bus Details', font='Arial 14 bold', bg='blue', fg='snow',command=main_to_addBusDetails ).grid(row=4, column=8)
        Label(root, text='\n',bg="light sky blue").grid(row=5, column=8)
        Label(root, text='For Admin Only', fg='blue4',bg="light sky blue",font='arial 10 bold').grid(row=6, column=8)

        root.mainloop()

    def seatBooking(self):
        root = Tk()
        root.title("Seat Booking")
        root.configure(bg="light sky blue")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))
        
        def seatBooking_to_main():
            root.destroy()
            self.main()

        def show_bus():
            tp=to_place.get()
            fp=from_place.get()
            jd=journey_date.get()

            if tp.isalpha() and fp.isalpha():
                if not jd=='':
                    tp = tp.lower()
                    fp = fp.lower()
                    cur.execute('select r_id from route where s_name=? and e_name=?', (fp, tp))
                    res_route = cur.fetchall()
                    if len(res_route)==0:
                        showerror('no route found','we are currently not running on this route')
                    else:
                        for i in res_route:
                            for j in i:
                                val_route = str(j)

                        cur.execute('select bus_id from bus where route_id=?', (val_route))
                        res_bid = cur.fetchall()

                        if len(res_bid)==0:
                            showerror('no bus found','we have not started any bus on this route yet!!')
                        else:
                            val_bid = []
                            for i in res_bid:
                                for j in i:
                                    val_bid.append(j)
                            res_new_bid=[]
                            for i in range(len(val_bid)):
                                cur.execute('select b_id from running where run_date=? and b_id=? ',(jd, val_bid[i]))
                                res_new_bid.append(cur.fetchall())
                            #print(res_new_bid)
                            b=[]
                            for i in res_new_bid:
                                for j in i:
                                    b.append(j[0])

                            #print(b)
                            if len(b)==0:
                                showerror('no running bus',"try another date!!")
                            else:
                                Label(root,text='Select bus ',font='Arial 12 bold', fg='blue',bg='light sky blue').grid(row=6,column=3,padx=20)
                                Label(root, text='Operator ', font='Arial 12 bold',fg='blue',bg='light sky blue').grid(row=6, column=4)
                                Label(root, text='Bus_Type ', font='Arial 12 bold',fg='blue',bg='light sky blue').grid(row=6, column=5)
                                Label(root, text='Available Capacity ', font='Arial 12 bold',fg='blue',bg='light sky blue').grid(row=6, column=6)
                                Label(root, text='Fare ', font='Arial 12 bold',fg='blue',bg='light sky blue').grid(row=6, column=7)
                                r=7
                                bus_no=IntVar()
                                bus_select = IntVar()
                                serial_no=1
                                for i in b:
                                    bus_no=i
                                    cur.execute('Select op_id from bus where bus_id=?',(i))
                                    res_opr_id=cur.fetchall()
                                    for j in res_opr_id:
                                        opr_id=j[0]

                                    cur.execute('Select name from operator where opr_id=?',(opr_id))
                                    res_opr_name=cur.fetchall()
                                    for j in res_opr_name:
                                        opr_name=j[0]

                                    cur.execute('Select bus_type from bus where bus_id=?',(i))
                                    res_bus_type=cur.fetchall()
                                    for j in res_bus_type:
                                        bus_type=j[0]

                                    cur.execute('Select seat_avail from running where run_date=? and b_id=?',(jd,i))
                                    res_seat_avail=cur.fetchall()
                                    for j in res_seat_avail:
                                        seat_avail=j[0]

                                    cur.execute('Select fair from bus where bus_id=?',(i))
                                    res_fare=cur.fetchall()
                                    for j in res_fare:
                                        fare=j[0]

                                    def show_button():
                                        Button(root, text='PROCEED', bg='blue', fg='snow', font='Arial 12 bold',command=proceed).grid(row=10, column=9, padx=30)

                                    var=Radiobutton(root,value=bus_no,variable=bus_select,command=show_button,bg="Light Sky Blue")
                                    var.grid(row=r,column=3,pady=5,padx=20)
                                    Label(root, text=opr_name, font='Arial 12 bold',bg="Light Sky Blue",fg='blue').grid(row=r, column=4,pady=5)
                                    Label(root, text=bus_type, font='Arial 12 bold',bg="Light Sky Blue",fg='blue').grid(row=r, column=5,pady=5)
                                    Label(root, text=seat_avail, font='Arial 12 bold',bg="Light Sky Blue",fg='blue').grid(row=r, column=6, pady=5)
                                    Label(root, text=fare, font='Arial 12 bold',bg="Light Sky Blue",fg='blue').grid(row=r, column=7,pady=5)

                                    r+=1
                                    serial_no+=1

                                def proceed():
                                    f_bus_id = bus_select.get()

                                    Label(root,text="\n",bg="Light Sky Blue").grid(row=10,columnspan=12)
                                    Label(root,text='Fill Passenger Details to Book the Seat', bg='SteelBlue1', fg='blue', font='Arial 15 bold').grid(row=11,columnspan=12)
                                    Label(root, text="\n",bg="Light Sky Blue").grid(row=12,columnspan=12)

                                    Label(root,text='Name',font='Arial 12 bold',bg='light sky blue').grid(row=13,column=3)
                                    pname = Entry(root, font='Arial 12 bold', fg='black')
                                    pname.grid(row=13,column=4)

                                    gender = StringVar()
                                    gender.set("Select Gender")
                                    opt = ["M", "F", "T"]
                                    g_menu = OptionMenu(root, gender, *opt)
                                    g_menu.grid(row=13, column=6)

                                    Label(root, text='Number of Seats', font='Arial 12 bold',bg='light sky blue').grid(row=13, column=7)
                                    pseat=Entry(root, font='Arial 12 bold', fg='black')
                                    pseat.grid(row=13,column=8)

                                    Label(root, text='Mobile', font='Arial 12 bold',bg='light sky blue').grid(row=14, column=3,pady=10)
                                    pmobile = Entry(root, font='Arial 12 bold', fg='black')
                                    pmobile.grid(row=14, column=4,pady=5)

                                    Label(root, text='Age', font='Arial 12 bold',bg='light sky blue').grid(row=14, column=5,pady=10)
                                    page = Entry(root, font='Arial 12 bold', fg='black')
                                    page.grid(row=14, column=6,pady=5)
                                    
                                    def generate_ticket_window(name, gen, age, mobile, seats, booking_ref, cur_date, jd, fare):
                                        ticket_window = Toplevel()
                                        ticket_window.title('Bus Ticket')
                                        ticket_window.geometry('500x400')
                                        ticket_window.configure(bg='light sky blue')
                                        
                                        Label(ticket_window, text='Bus Ticket', font='Arial 20 bold',bg='steelblue1',fg='blue').pack(pady=20)

                                        Label(ticket_window, text=f'Booking Ref : {booking_ref}', font='Arial 12 bold',bg='light sky blue',fg='black').pack(pady=10)
                                        Label(ticket_window, text=f'Name : {name}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()
                                        Label(ticket_window, text=f'Gender : {gen}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()
                                        Label(ticket_window, text=f'Age : {age}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()
                                        Label(ticket_window, text=f'Mobile : {mobile}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()
                                        Label(ticket_window, text=f'Number of Seats : {seats}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()
                                        Label(ticket_window, text=f'Booking Date : {cur_date}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()
                                        Label(ticket_window, text=f'Travel Date : {jd}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()
                                        Label(ticket_window, text=f'Fare : {fare}', font='Arial 12 bold',bg='light sky blue',fg='black').pack()

                                        def close_window():
                                            ticket_window.destroy()

                                        Button(ticket_window, text='Close',bg='blue',fg='snow', command=close_window,font='arial 12 bold').pack(pady=20)

                                        ticket_window.mainloop()


                                    def book_seat():
                                        name=pname.get()
                                        gen=gender.get()
                                        seats=pseat.get()
                                        seats=int(seats)
                                        age=page.get()
                                        age=int(age)
                                        mobile=pmobile.get()
                                        bid=bus_select.get()
                                        if len(mobile)==10:
                                            if len(name)>0 and len(name)<20:
                                                if age>0 and age<100:
                                                    if seats>0 and seats<42:
                                                        #print(name, gen, age, mobile, seats, bid)
                                                        booking_ref=1
                                                        cur.execute('select booking_ref from booking_history')
                                                        res_ref=cur.fetchall()
                                                        ref=[]
                                                        for i in res_ref:
                                                            ref.append(i[0])
                                                        booking_ref=len(ref)+1
                                                        #print(booking_ref)
                                                        cur_date=date.today()
                                                        cur.execute('insert into booking_history(name,gender,no_of_seat,phone,age,booking_ref,booking_date,travel_date,bid) values(?,?,?,?,?,?,?,?,?)',(name,gen,seats,mobile,age,booking_ref,cur_date,jd,bid))
                                                        con.commit()
                                                        cur.execute('select seat_avail from running where b_id=? and run_date=?',(bid,jd))
                                                        res_s=cur.fetchall()
                                                        s=res_s[0][0]
                                                        s=s-seats
                                                        cur.execute('update running set seat_avail=? where b_id=? and run_date=?',(s,bid,jd))
                                                        con.commit()
                                                        showinfo("successfull","booking successfull")
                                                        generate_ticket_window(name, gen, age, mobile, seats, booking_ref, cur_date, jd, fare)

                                                    else:
                                                        showerror("booking limit exceed","you can only book upto 40 seats")
                                                else:
                                                    showerror("incorrect age","enter valid age")
                                            else:
                                                showerror("incorrect name","enter valid name")
                                        else:
                                            showerror("invalid mobile no","enter valid mobile no")


                                    Button(root, text='BOOK SEAT', bg='blue', fg='snow', font='Arial 12 bold',command=book_seat).grid(row=14, column=9, padx=30)



                else:
                    showerror('error','Enter journey date')


            else:
                showerror('ERROR',"Enter correctly!!")


        bus = PhotoImage(file='starbus.png')
        Label(root, image=bus,bg="light sky blue").grid(row=0, column=3, columnspan=12)
        Label(root, text=" Online Bus Booking System ", font='Arial 25 bold', bg='azure', fg='blue4').grid(row=2, column=3, pady=10, columnspan=12)
        Label(root, text='Enter Journey Details', bg='SteelBlue1', fg='Blue', font='Arial 15 bold').grid(row=3, column=3, columnspan=12, pady=10)
        Label(root, text='To', fg='black', font='Arial 12 bold',bg="light sky blue").grid(row=4, column=3, padx=30)
        to_place = Entry(root, font='Arial 12 bold', fg='black')
        to_place.grid(row=4, column=4, padx=50)

        Label(root, text='From', fg='black', font='Arial 12 bold',bg="light sky blue").grid(row=4, column=5, padx=30)
        from_place = Entry(root, font='Arial 12 bold', fg='black')
        from_place.grid(row=4, column=6, padx=50)

        Label(root, text='Journey Date', fg='black', font='Arial 12 bold',bg="light sky blue").grid(row=4, column=7, padx=30)
        journey_date = Entry(root, font='Arial 12 bold', fg='black')
        journey_date.grid(row=4, column=8, padx=50)
        Label(root,text="Date Format : YYYY-MM-DD",bg="light sky blue",fg='black',font='arial 8 bold').grid(row=5,column=8)

        Button(root, text='Show Bus', bg='blue', fg='snow', font='Arial 12 bold',command=show_bus).grid(row=4, column=9, padx=30)

        home = PhotoImage(file='home.png')

        Button(root, image=home,command=seatBooking_to_main).grid(row=4, column=10)

        root.mainloop()

    def checkBooking(self):
        root = Tk()
        root.title("Check Booking")
        root.configure(bg="light sky blue")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))
        bus = PhotoImage(file='starbus.png')
        home=PhotoImage(file='home.png')

        def checkBooking_to_main():
            root.destroy()
            self.main()

        def check_tkt():
            mobile = mob.get()
            if len(mobile) == 10 and mobile.isdigit():
                cur.execute('select * from booking_history where phone=?', [mobile])
                res_tkt = cur.fetchall()
                if not res_tkt:
                    showerror("Booking Not Found", "No booking found for this phone number")
                    return
                for i in res_tkt:
                    name=i[0]
                    gen=i[1]
                    seat=i[2]
                    phone=i[3]
                    age=i[4]
                    ref=i[5]
                    book_date=i[6]
                    travel_date=i[7]
                    b_i_d=i[8]
                cur.execute('select fair,route_id from bus where bus_id=?',[b_i_d])
                res_bus=cur.fetchall()
                fare=res_bus[0][0]
                route_id=res_bus[0][1]
                cur.execute('select s_name,e_name from route where r_id=?',[route_id])
                res_route=cur.fetchall()
                s_name=res_route[0][0]
                e_name=res_route[0][1]
                cur.execute('select booking_ref from booking_history where phone=?',[phone])
                res_ref=cur.fetchall()
                b_ref=res_ref[0][0]

                Label(text="YOUR TICKET", font='Arial 12 bold', bg='blue',fg='white').grid(row=6,columnspan=12 )
                Label(text="Booking Ref : "+b_ref,font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=7,column=4,pady=20)
                Label(text="Name : " + name, font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=7, column=5)
                Label(text="Gender : " + gen, font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=7, column=6)
                Label(text="No. of Seats : " + str(seat), font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=7, column=7)
                Label(text="Age : " + str(age), font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=7, column=8)
                Label(text="Booked On : " + book_date, font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=8, column=4)
                Label(text="Travel Date : " + travel_date, font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=8, column=5)
                Label(text="Fare : " + str(fare), font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=8, column=6)
                Label(text="Total Fare : " + str(fare*seat), font='Arial 12 bold', fg='blue',bg="light sky blue").grid(row=8, column=7)

            else:
                showerror("Invalid Mobile No", "Please enter a valid 10-digit mobile number")
     




        Label(root, image=bus,bg="light sky blue").grid(row=0, column=0, columnspan=12, padx=80)
        Label(root, text=" Online Bus Booking System ", font='Arial 28 bold', bg='azure', fg='blue4').grid(row=2, column=0, columnspan=12, pady=20)
        Label(root, text="Check Your Booking", font='Arial 22 bold', bg='SteelBlue1', fg='blue').grid(row=3, column=0, pady=20, columnspan=12, padx=600)
        Label(root, text="Enter Your Mobile No.", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=4, column=5)
        mob=Entry(root, font='Arial 12 bold')
        mob.grid(row=4, column=6)

        Button(root, text='Check Booking', font='Arial 12 bold',command=check_tkt,bg='blue',fg='snow').grid(row=4, column=7)
        Button(root, image=home,command=checkBooking_to_main).grid(row=5, column=7,pady=20)
        root.mainloop()

    def addBusDetails(self):
        root = Tk()
        root.title("Admin")
        root.configure(bg="light sky blue")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))

        bus = PhotoImage(file='.\\starbus.png')

        def addBusDetails_to_newOperator():
            root.destroy()
            self.newOperator()

        def addBusDetails_to_newBus():
            root.destroy()
            self.newBus()

        def addBusDetails_to_newRoute():
            root.destroy()
            self.newRoute()

        def addBusDetails_to_newRun():
            root.destroy()
            self.newRun()

        Label(root, text='\n\n\n\n').grid(row=0, column=0)
        Label(root, image=bus,bg="light sky blue").grid(row=1, column=1, columnspan=12, padx=w // 2.5)
        Label(root, text=" Online Bus Booking System ", font='Arial 20 bold', bg='azure', fg='blue4').grid(row=2,column=2, columnspan=9, padx=w // 2.5)
        Label(root, text='\n',bg="light sky blue").grid(row=3, column=2)
        Label(root, text="Add New Details To Database", font='Arial 16 bold', bg='SteelBlue1', fg='blue').grid(row=4, column=2,columnspan=9, padx=w // 2.5)
        Label(root, text='\n',bg="light sky blue").grid(row=5, column=2)

        Button(root, text='New Operator', fg='snow', bg='blue', font='Arial 12 bold',command=addBusDetails_to_newOperator).grid(row=6, column=1,columnspan=7)
        Button(root, text='New Bus', fg='snow', bg='blue', font='Arial 12 bold',command=addBusDetails_to_newBus).grid(row=6, column=5, columnspan=2)
        Button(root, text='New Route', fg='snow', bg='blue', font='Arial 12 bold',command=addBusDetails_to_newRoute).grid(row=6, column=6, columnspan=2)
        Button(root, text='New Run', fg='snow', bg='blue', font='Arial 12 bold',command=addBusDetails_to_newRun).grid(row=6, column=7, columnspan=2)

        root.mainloop()

    def newOperator(self):
        root = Tk()
        root.title("Operator Details")
        root.configure(bg="light sky blue")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))

        bus = PhotoImage(file='starbus.png')
        home=PhotoImage(file='home.png')

        def op_add():
            iid = opr_id.get()
            iname = name.get()
            iaddress = address.get()
            iphone = phone.get()
            iemail = email.get()
            cur.execute('select opr_id from operator')
            res=cur.fetchall()
            
            if len(iid) > 0 and len(iid) <= 5 and iid.isnumeric():
                if  len(iname) < 20 and len(iname) > 0:
                    if len(iaddress) < 50 and len(iaddress) > 0:
                        if iphone.isnumeric() and len(iphone) == 10:
                            if len(iemail) > 0 and len(iemail) < 30:
                                if (iid,) in res:
                                    showerror("ERROR","operator id already exists!!")
                                else:
                                    cur.execute('insert into operator (opr_id,name,address,phone,email)values(?,?,?,?,?)',(iid, iname, iaddress, iphone, iemail))
                                    con.commit()
                                    showinfo('success', "operator added successfully!!")

                                
                            else:
                                showerror("invalid input", "enter email correctly")
                        else:
                            showerror("invalid input", "enter phone correctly")
                    else:
                        showerror("invalid input", "enter address correctly")
                else:
                    showerror("invalid input", "enter name correctly")
            else:
                showerror("invalid input", "enter id correctly")
                
        def op_edit():
            def retrieve_op_details():
                operator_id = opr_id.get()
                cur.execute('SELECT * FROM operator WHERE opr_id=?', (operator_id,))
                fetched_op = cur.fetchone()

                if fetched_op:
                    name.delete(0, END)
                    address.delete(0, END)
                    phone.delete(0, END)
                    email.delete(0, END)

                    name.insert(END, fetched_op[1])
                    address.insert(END, fetched_op[2])
                    phone.insert(END, fetched_op[3])
                    email.insert(END, fetched_op[4])
                    update_op_details()   
                else:
                    showerror("Operator not found", "Operator ID not found in the database")

            def update_op_details():
                operator_id = opr_id.get()
                new_name = name.get()
                new_address = address.get()
                new_phone = phone.get()
                new_email = email.get()

                cur.execute('UPDATE operator SET name=?, address=?, phone=?, email=? WHERE opr_id=?',
                            (new_name, new_address, new_phone, new_email, operator_id))
                con.commit()
                showinfo("Success", "Operator details updated successfully")
                
            retrieve_op_details()     


        def newOperator_to_main():
            root.destroy()
            self.main()

        Label(root, image=bus,bg="light sky blue").grid(row=0, column=0, columnspan=12)
        Label(root, text=" Online Bus Booking System ", font='Arial 28 bold', bg='azure', fg='blue4').grid(row=1, column=0, columnspan=12)
        Label(root, text="Add Bus Operator Details", font='Arial 20 bold', bg='SteelBlue1', fg='blue').grid(row=2, column=0, pady=20, columnspan=12)
        Label(root, text="Operator ID", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=0, pady=50, padx=5)
        opr_id = Entry(root, font="Arial 12 bold")
        opr_id.grid(row=3, column=1,padx=5)
        Label(root, text="Name", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=2,padx=5)
        name = Entry(root, font="Arial 12 bold")
        name.grid(row=3, column=3,padx=5)
        Label(root, text="Address", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=4,padx=5)
        address = Entry(root, font="Arial 12 bold")
        address.grid(row=3, column=5,padx=5)
        Label(root, text="Phone", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=6,padx=5)
        phone = Entry(root, font="Arial 12 bold")
        phone.grid(row=3, column=7,padx=5)
        Label(root, text="Email", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=8,padx=5)
        email =  Entry(root, font="Arial 12 bold")
        email.grid(row=3, column=9,padx=5)



        Button(root, text="Add", font='Arial 12 bold', bg='blue', fg='snow',command=op_add).grid(row=3, column=10, padx=20)
        Button(root, text="Edit", font='Arial 12 bold', bg='blue', fg='snow',command=op_edit).grid(row=3, column=11, padx=10)

        
        Button(root, image=home,command=newOperator_to_main).grid(row=7, column=11)
        root.mainloop()

    def newBus(self):
        root = Tk()
        root.title("Bus Details")
        root.configure(bg="light sky blue")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))

        bus = PhotoImage(file='starbus.png')
        
        def bus_add():
            bid=b_id.get()
            dmenu=bus_type.get()
            capa=capacity.get()
            fare_rs=fare.get()
            opid=op_id.get()
            route_id=r_id.get()
            cur.execute('select bus_id from bus')
            res=cur.fetchall()
            if (bid,) in res:
                showerror("error","bus id already exists!!!")
            else:
                data="Bus ID = "+bid+"     Bus Type = "+dmenu+"     Capacity = "+capa+"     Fare = "+fare_rs+"     Operator ID = "+opid+"     Route ID = "+route_id
                cur.execute('insert into bus(bus_id,bus_type,capacity,fair,op_id,route_id) values(?,?,?,?,?,?)',(bid,dmenu,capa,fare_rs,opid,route_id))
                con.commit()
                showinfo('success', "bus added successfully!!")
                Label(root,text=data).grid(row=6,columnspan=12)
                
        def edit_bus():
            bid = b_id.get()
            dmenu = bus_type.get()
            capa = capacity.get()
            fare_rs = fare.get()
            opid = op_id.get()
            route_id = r_id.get()

            cur.execute('SELECT bus_id FROM bus')
            res = cur.fetchall()
            
            if (bid,) in res:
                data = "BUS ID = {}  BUS TYPE = {}  Capacity = {}  Fare = {}  Operator ID = {}  Route ID = {}".format(bid, dmenu, capa, fare_rs, opid, route_id)
                
                cur.execute('UPDATE bus SET bus_type=?, capacity=?, fair=?, op_id=?, route_id=? WHERE bus_id=?',(dmenu, capa, fare_rs, opid, route_id, bid))
                
                con.commit() 
                
                Label(root, text=data,font="arial 12 bold",bg="Bisque").grid(row=6, columnspan=12)
            else:
                showerror("Error", "No such bus ID exists. Please add a new bus.")

        def newBus_to_main():
            root.destroy()
            self.main()

        Label(root, image=bus,bg="light sky blue").grid(row=0, column=0, columnspan=12)
        Label(root, text=" Online Bus Booking System ", font='Arial 28 bold', bg='azure', fg='blue4').grid(row=1, column=0, columnspan=12)
        Label(root, text="Add Bus Details", font='Arial 20 bold', bg='SteelBlue1', fg='blue').grid(row=2, column=0, pady=20,columnspan=12)
        Label(root, text="Bus ID", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=1, pady=50,padx=5)
        b_id = Entry(root, font="Arial 12 bold")
        b_id.grid(row=3, column=2,padx=5)

        bus_type = StringVar()
        bus_type.set("Select Bus Type")
        opt = ["2x2", "AC 2x2", "3x2", "AC 3x2"]
        d_menu = OptionMenu(root, bus_type, *opt)
        d_menu.grid(row=3, column=3,padx=5)
        
        Label(root, text="Capacity", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=4,padx=5)
        capacity = Entry(root, font="Arial 12 bold")
        capacity.grid(row=3, column=5,padx=5)
        
        Label(root, text="Fare Rs", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=6,padx=5)
        fare = Entry(root, font="Arial 12 bold")
        fare.grid(row=3, column=7,padx=5)
        
        Label(root, text="Operator ID", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=8,padx=5)
        op_id = Entry(root, font="Arial 12 bold")
        op_id.grid(row=3, column=9,padx=5)
        
        Label(root, text="Route ID", font='Arial 12 bold', fg='black',bg="light sky blue").grid(row=3, column=10,padx=5)
        r_id = Entry(root, font="Arial 12 bold")
        r_id.grid(row=3, column=11,padx=5)

        Button(root, text="Add Bus", font='Arial 12 bold', bg='blue', fg='snow',command=bus_add).grid(row=5, column=4, pady=20, columnspan=4)
        Button(root, text="Edit Bus", font='Arial 12 bold', bg='blue', fg='snow',command=edit_bus).grid(row=5, column=5, pady=20, columnspan=4,padx=10)

        home = PhotoImage(file='home.png')
        Button(root, image=home,command=newBus_to_main).grid(row=5, column=6, columnspan=3)
        
        
        root.mainloop()

    def newRoute(self):

        root=Tk()
        root.title("Route Details")
        root.configure(bg="light sky blue")
        def newRoute_to_main():
            root.destroy()
            self.main()
        def add_route():
            route_id=r_id.get()
            start_station=s_station.get()
            start_id=s_id.get()
            end_station=e_station.get()
            end_id=e_id.get()

            cur.execute('select r_id from route')
            res=cur.fetchall()
            if (route_id,) in res:
                showerror('ERROR',"Route id already exists")
            else:
                start_station=start_station.lower()
                end_station=end_station.lower()
                cur.execute('insert into route(r_id,s_name,s_id,e_name,e_id) values(?,?,?,?,?)',(route_id,start_station,start_id,end_station,end_id))
                con.commit()
                showinfo('success',"route added successfully!!")
                
        def delete_route():
            route_id = r_id.get()

            cur.execute('SELECT r_id FROM route')
            res = cur.fetchall()

            if (route_id,) in res:
                cur.execute('DELETE FROM route WHERE r_id=?', (route_id,))
                con.commit()
                showinfo('Success', 'Route deleted successfully!!')
            else:
                showerror('Error', 'Route ID does not exist. Please enter a valid Route ID.')        

        h,w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))

        bus = PhotoImage(file='starbus.png')
        Label(root, image=bus,bg="light sky blue").grid(row=0, column=0, columnspan=12)
        Label(root, text=" Online Bus Booking System ", font='Arial 28 bold', bg='azure', fg='blue4').grid(row=1, column=0, columnspan=12)
        Label(root, text="Add Bus Route Details", font='Arial 20 bold', bg='SteelBlue1', fg='blue').grid(row=2, column=0, pady=20, columnspan=12)

        Label(root, text="Route ID", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=3, column=0, pady=50, padx=50)
        r_id=Entry(root, font="Arial 12 bold")
        r_id.grid(row=3, column=1, padx=30)

        Label(root, text="Starting Station", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=3, column=2)
        s_station=Entry(root, font="Arial 12 bold")
        s_station.grid(row=3, column=3, padx=50)

        Label(root, text="Station ID", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=3, column=4)
        s_id=Entry(root, font="Arial 12 bold")
        s_id.grid(row=3, column=5, padx=50)

        Label(root, text="Ending Station", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=4, column=2)
        e_station=Entry(root, font="Arial 12 bold")
        e_station.grid(row=4, column=3, padx=50)

        Label(root, text="Station ID", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=4, column=4)
        e_id=Entry(root, font="Arial 12 bold")
        e_id.grid(row=4, column=5, padx=50)

        Button(root, text="Add Route", font='Arial 12 bold', bg='blue', fg='snow',command=add_route).grid(row=3, column=7, pady=20, padx=10)
        Button(root, text="Delete Route", font='Arial 12 bold', bg='blue', fg='snow',command=delete_route).grid(row=3, column=9, pady=20, padx=10)

        home = PhotoImage(file='home.png')
        Button(root, image=home,command=newRoute_to_main).grid(row=4, column=9)

        root.mainloop()

    def newRun(self):
        root = Tk()
        root.title("Run Details")
        root.configure(bg="light sky blue")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry('%dx%d+0+0' % (w, h))

        bus = PhotoImage(file='starbus.png')

        def newRun_to_main():
            root.destroy()
            self.main()
            
        def add_run():
            bid = bus_id.get()
            run_date = running_date.get()
            s_avail = seat_avail.get()

            cur.execute('SELECT b_id, run_date FROM running WHERE b_id=? AND run_date=?', (bid, run_date))
            res = cur.fetchall()

            if res:
                showerror('Error', 'Run already exists for the specified Bus ID and Running Date!')
            else:
                cur.execute('INSERT INTO running(b_id, run_date, seat_avail) VALUES (?, ?, ?)', (bid, run_date, s_avail))
                con.commit()
                showinfo('Success', 'Run added successfully!!')
            
        def delete_run():
            bid = bus_id.get()
            run_date = running_date.get()

            cur.execute('SELECT b_id, run_date FROM running')
            res = cur.fetchall()

            if (bid, run_date) in res:
                cur.execute('DELETE FROM running WHERE b_id=? AND run_date=?', (bid, run_date))
                con.commit()
                showinfo('Success', 'Run deleted successfully!!')
            else:
                showerror('Error', 'No such Run ID exists. Please enter a valid Bus ID and Running Date.')    

        Label(root, image=bus,bg="light sky blue").grid(row=0, column=0, columnspan=12)
        Label(root, text=" Online Bus Booking System ", font='Arial 28 bold', bg='azure', fg='blue4').grid(row=1, column=0, columnspan=12)
        Label(root, text="Add Bus Running Details", font='Arial 20 bold', bg='SteelBlue1', fg='blue').grid(row=2,column=0, pady=20, columnspan=12)
        
        Label(root, text="Bus ID", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=3, column=1, pady=50, padx=50)
        bus_id=Entry(root, font="Arial 12 bold")
        bus_id.grid(row=3, column=2, padx=50)

        Label(root, text="Running Date", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=3, column=3)
        running_date=Entry(root, font="Arial 12 bold")
        running_date.grid(row=3, column=4, padx=50)
        Label(root,text="Date Format : YYYY-MM-DD",font = 'arial 8 bold',bg='light sky blue').grid(row=4,column=4)

        Label(root, text="Seat Available", font='Arial 12 bold', fg='black',bg='light sky blue').grid(row=3, column=5)
        seat_avail=Entry(root, font="Arial 12 bold")
        seat_avail.grid(row=3, column=6, padx=50)

        Button(root, text="Add Run", font='Arial 12 bold', bg='blue', fg='snow',command=add_run).grid(row=3, column=7, pady=20, padx=10)
        Button(root, text="Delete Run", font='Arial 12 bold', bg='blue', fg='snow',command=delete_run).grid(row=3, column=8, pady=20,padx=10)

        home = PhotoImage(file='home.png')

        Button(root, image=home,command=newRun_to_main).grid(row=4, column=8)

        root.mainloop()

obj=onlineBusBookingSystem()
obj.home()

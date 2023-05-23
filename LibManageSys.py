import re
import speech_recognition as sr
import pyttsx3
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msg
import threading
import keyboard
import mysql.connector
from PIL import ImageTk, Image
import smtplib
from datetime import datetime
import datetime

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="digital_library"
)
flag = [0, 0]
current = ["pressed_button", "login_name", "login_email", "login_member", "book_name", "author_name"]

def background(self):
    background_image = ImageTk.PhotoImage(Image.open('book.jpg'))
    background_label = Label(self, image=background_image)
    background_label.image = background_image
    background_label.pack()

def first_page():
    self = Tk()
    self.geometry("800x800")
    self.title("Library Management System")
    background(self)
    heading = Label(self, text="Central Library", fg="white", bg="black", font=("bold", 30))
    heading.place(x=280, y=10)
    login = Label(self, text="Login as:", fg="white", bg="black", font=20)
    login.place(x=380, y=160)
    student_button = Button(self, text="Student", font=20, command=lambda flg1=5: threading.Thread(target=middle_pages(flg1)))
    student_button.place(x=250, y=390)
    student_logo = Canvas(self, width=130, height=150, bg="black")
    student_logo.place(x=220, y=220)
    half_oval1 = Label(self, text="O", fg="white", bg="black", font=("bold", 70))
    half_oval1.place(x=250, y=250)
    oval1 = Label(self, text="O", fg="white", bg="black", font=("bold", 56))
    oval1.place(x=257, y=225)
    librarian_button = Button(self, text="Librarian", font=20, command=lambda flg2=2: threading.Thread(target=middle_pages(flg2)))
    librarian_button.place(x=500, y=390)
    librarian_logo = Canvas(self, width=130, height=150, bg="black")
    librarian_logo.place(x=470, y=220)
    half_oval2 = Label(self, text="O", fg="white", bg="black", font=("bold", 70))
    half_oval2.place(x=500, y=250)
    oval2 = Label(self, text="O", fg="white", bg="black", font=("bold", 56))
    oval2.place(x=507, y=225)
    menubutton = Menubutton(self, text="Menu", font=15)
    menubutton.menu = Menu(menubutton)
    menubutton["menu"] = menubutton.menu
    menubutton.menu.add_command(label="New Registration", command=lambda flg3=3: threading.Thread(target=middle_pages(flg3)))
    menubutton.menu.add_command(label="Delete Member", command=lambda flg3=4: threading.Thread(target=middle_pages(flg3)))
    menubutton.menu.add_command(label="About", command=lambda flg3=7: threading.Thread(target=middle_pages(flg3)))
    menubutton.place(x=100, y=80)
    exit_button = Button(self, text="Exit", font=20, command=self.destroy)
    exit_button.place(x=100, y=500)
    self.bind('<Escape>', lambda event: self.destroy())
    self.mainloop()

def middle_pages(flg):
    self = Toplevel()
    self.geometry("800x800")
    self.title("Library Management System")
    background(self)
    if flg == 1:
        if 'normal' == self.state():
            self.focus_force()
        heading = Label(self, text="Student Login Page", fg="white", bg="black", font=("bold", 20))
        heading.place(x=280, y=10)
        st_email = Label(self, text="Student Email:", fg="black", bg="grey", font=15)
        st_email.place(x=280, y=240)
        self.st_email = Entry(self)
        self.st_email.place(x=400, y=242)
        st_password = Label(self, text="Enter password:", fg="black", bg="grey", font=15)
        st_password.place(x=280, y=280)
        self.st_password = Entry(self, show="*")
        self.st_password.place(x=400, y=282)
        def st_login():
            c1 = my_db.cursor()
            c1.execute("select Member_Name, Member_Type, Password from members where email_id=%s", (self.st_email.get(),))
            member_name = ""
            member_type = ""
            get_password = ""
            for a in c1:
                member_name = a[0]
                member_type = a[1]
                get_password = a[2]
            if member_type == "student":
                if get_password == self.st_password.get():
                    current[1] = member_name
                    current[2] = self.st_email.get()
                    current[3] = "student"
                    self.destroy()
                    threading.Thread(target=speak("login as a student!"))
                    msg.showinfo("login", "Login as Student")
                    threading.Thread(target=middle_pages(5))
                else:
                    msg.showerror("error", "Password is Incorrect!")
                    self.focus_force()
            elif member_type == "librarian":
                msg.showerror("login error", "Invalid Member!")
                self.focus_force()
            else:
                msg.showerror("system error", "Invalid Credential!")
                self.focus_force()
        next_button = Button(self, text="Next", font=20, command=st_login)
        next_button.place(x=600, y=500)
        self.bind('<Return>', lambda event: st_login())
        back_button = Button(self, text="Back", font=20, command=self.destroy)
        back_button.place(x=100, y=500)
        self.bind('<Escape>', lambda event: self.destroy())
    elif flg == 2:
        if 'normal' == self.state():
            self.focus_force()
        heading = Label(self, text="Librarian Login Page", fg="white", bg="black", font=("bold", 20))
        heading.place(x=280, y=10)
        lb_email = Label(self, text="Librarian Email:", fg="black", bg="grey", font=15)
        lb_email.place(x=260, y=240)
        self.lb_email = Entry(self)
        self.lb_email.place(x=400, y=242)
        lb_password = Label(self, text="Enter password:", fg="black", bg="grey", font=15)
        lb_password.place(x=260, y=280)
        self.lb_password = Entry(self, show="*")
        self.lb_password.place(x=400, y=282)
        def lb_login():
            c1 = my_db.cursor()
            c1.execute("select Member_Name, Member_Type, Password from members where email_id=%s", (self.lb_email.get(),))
            member_name = ""
            member_type = ""
            get_password = ""
            for a in c1:
                member_name = a[0]
                member_type = a[1]
                get_password = a[2]
            if member_type == "librarian":
                if get_password == self.lb_password.get():
                    current[1] = member_name
                    current[2] = self.lb_email.get()
                    current[3] = "librarian"
                    self.destroy()
                    threading.Thread(target=speak("login as a librarian!"))
                    msg.showinfo("login", "Login as librarian")
                    threading.Thread(target=middle_pages(6))
                else:
                    msg.showerror("error", "Password is Incorrect!")
                    self.focus_force()
            elif member_type == "student":
                msg.showerror("login error", "Invalid Member!")
                self.focus_force()
            else:
                msg.showerror("system error", "Invalid Credential!")
                self.focus_force()
        next_button = Button(self, text="Next", font=20, command=lb_login)
        next_button.place(x=600, y=500)
        self.bind('<Return>', lambda event: lb_login())
        back_button = Button(self, text="Back", font=20, command=self.destroy)
        back_button.place(x=100, y=500)
        self.bind('<Escape>', lambda event: self.destroy())
    elif flg == 3:
        if 'normal' == self.state():
            self.focus_force()
        heading = Label(self, text="Registration", fg="white", bg="black", font=("bold", 25))
        heading.place(x=270, y=10)
        name = Label(self, text="Enter Name:", fg="black", bg="grey", font=15)
        name.place(x=250, y=198)
        self.name = Entry(self)
        self.name.place(x=400, y=200)
        email_id = Label(self, text="Enter Email:", fg="black", bg="grey", font=15)
        email_id.place(x=250, y=240)
        self.email_id = Entry(self)
        self.email_id.place(x=400, y=242)
        member = Label(self, text="Member type:", fg="black", bg="grey", font=15)
        member.place(x=250, y=280)
        self.member = Entry(self)
        self.member.place(x=400, y=279)
        password = Label(self, text="Enter Password:", fg="black", bg="grey", font=15)
        password.place(x=250, y=320)
        self.password = Entry(self, show="*")
        self.password.place(x=400, y=320)
        conf_password = Label(self, text="Confirm Password:", fg="black", bg="grey", font=15)
        conf_password.place(x=250, y=360)
        self.conf_password = Entry(self, show="*")
        self.conf_password.place(x=400, y=361)
        def state():
            while True:
                if self.name.get() == "" or self.email_id.get() == "" or self.member.get() == "" or self.password.get() == "" or self.conf_password.get() == "":
                    submit_button['state'] = DISABLED
                else:
                    submit_button['state'] = ACTIVE
                    break
        def data_register():
            if "@gmail.com" not in self.email_id.get():
                msg.showerror("System error", "Enter valid Email Address!")
                self.focus_force()
            elif len(self.password.get()) < 8:
                msg.showerror("error", "password should have minimum length 8!")
                self.focus_force()
            elif not re.search("[_@$]", self.password.get()):
                msg.showerror("error", "password should contain at least one special character!")
                self.focus_force()
            elif not re.search("[a-z]", self.password.get()):
                msg.showerror("error", "password should contain at least one lower case letter!")
                self.focus_force()
            elif not re.search("[A-Z]", self.password.get()):
                msg.showerror("error", "password should contain at least one upper case letter!")
                self.focus_force()
            elif not re.search("[0-9]", self.password.get()):
                msg.showerror("error", "password should contain at least one number!")
                self.focus_force()
            elif re.search("\s", self.password.get()):
                msg.showerror("error", "password should not contain any spaces!")
                self.focus_force()
            elif self.password.get() != self.conf_password.get():
                msg.showerror("error", "confirm password again!")
                self.focus_force()
            else:
                c = my_db.cursor()
                c.execute("Insert into members values(NULL, %s, %s, %s, %s)", (self.name.get(), self.email_id.get(), self.member.get(), self.password.get()))
                my_db.commit()
                self.destroy()
                threading.Thread(target=speak("Member added successfully!"))
                msg.showinfo("Registration", "Member added successfully!")
        submit_button = Button(self, text="Submit", font=20, command=data_register, state=DISABLED)
        submit_button.place(x=600, y=500)
        self.bind('<Return>', lambda event: data_register())
        threading.Thread(target=state).start()
        back_button = Button(self, text="Back", font=20, command=self.destroy)
        back_button.place(x=100, y=500)
        self.bind('<Escape>', lambda event: self.destroy())
    elif flg == 4:
        if 'normal' == self.state():
            self.focus_force()
        heading = Label(self, text="Delete Member", fg="white", bg="black", font=("bold", 25))
        heading.place(x=300, y=10)
        member_name = Label(self, text="Enter Member Name:", fg="black", bg="grey", font=15)
        member_name.place(x=240, y=198)
        self.member_name = Entry(self)
        self.member_name.place(x=400, y=200)
        email_id = Label(self, text="Enter Member Email:", fg="black", bg="grey", font=15)
        email_id.place(x=240, y=240)
        self.email_id = Entry(self)
        self.email_id.place(x=400, y=242)
        security_key = Label(self, text="Enter Security Key:", fg="black", bg="grey", font=15)
        security_key.place(x=240, y=280)
        self.security_key = Entry(self, show="*")
        self.security_key.place(x=400, y=282)
        def delete_data():
            my_c = my_db.cursor()
            if self.security_key.get() == "Library":
                try:
                    my_c.execute("DELETE from members where Member_Name=%s and Email_Id=%s", (self.member_name.get(), self.email_id.get()))
                    my_db.commit()
                    self.destroy()
                    threading.Thread(target=speak("Member is Deleted from the record!"))
                    msg.showinfo("notification", "Member is Deleted from the record!")
                    self.focus_force()
                except:
                    msg.showerror("error", "Enter valid Information")
                    self.focus_force()
            else:
                msg.showerror("error", "Enter valid Security Key")
                self.focus_force()
        submit_button = Button(self, text="Submit", font=20, command=delete_data)
        submit_button.place(x=600, y=500)
        self.bind('<Return>', lambda event: data_register())
        back_button = Button(self, text="Back", font=20, command=self.destroy)
        back_button.place(x=100, y=500)
        self.bind('<Escape>', lambda event: self.destroy())
    elif flg == 5:
        def buttons():
            background(self)
            list_button = Button(self, text="List of Books", font=5, command=lambda flg5=1: threading.Thread(target=frames(flg5)))
            list_button.place(x=0, y=0)
            issue_button = Button(self, text="Issue Books", font=5, command=lambda flg5=4: threading.Thread(target=frames(flg5)))
            issue_button.place(x=106, y=0)
            return_button = Button(self, text="Return Books", font=5, command=lambda flg5=5: threading.Thread(target=frames(flg5)))
            return_button.place(x=205, y=0)
            welcome = Label(self, text=f"Welcome {current[1]}", fg="white", bg="red", font=("bold", 15))
            welcome.place(x=600, y=5)
            back_button = Button(self, text="Back", font=20, command=self.destroy)
            back_button.place(x=100, y=540)
            self.bind('<Escape>', lambda event: self.destroy())
        def clear():
            for widget in self.winfo_children():
                widget.destroy()
        def frames(no):
            if no == 1:
                clear()
                buttons()
                last_pages(self, 1)
            elif no == 4:
                clear()
                buttons()
                last_pages(self, 4)
            elif no == 5:
                clear()
                buttons()
                last_pages(self, 5)
        buttons()
        frames(1)
    elif flg == 6:
        def buttons():
            background(self)
            list_button = Button(self, text="List of Books", font=5, command=lambda flg6=1: threading.Thread(target=frames(flg6)))
            list_button.place(x=0, y=0)
            add_button = Button(self, text="Add Books", font=5, command=lambda flg6=2: threading.Thread(target=frames(flg6)))
            add_button.place(x=105, y=0)
            delete_button = Button(self, text="Delete Books", font=5, command=lambda flg6=3: threading.Thread(target=frames(flg6)))
            delete_button.place(x=197, y=0)
            issue_button = Button(self, text="Issue Books", font=5, command=lambda flg6=4: threading.Thread(target=frames(flg6)))
            issue_button.place(x=305, y=0)
            return_button = Button(self, text="Return Books", font=5, command=lambda flg6=5: threading.Thread(target=frames(flg6)))
            return_button.place(x=404, y=0)
            welcome = Label(self, text=f"Welcome {current[1]}", fg="white", bg="red", font=("bold", 15))
            welcome.place(x=600, y=5)
            back_button = Button(self, text="Back", font=20, command=self.destroy)
            back_button.place(x=100, y=540)
            self.bind('<Escape>', lambda event: self.destroy())
        def clear():
            for widget in self.winfo_children():
                widget.destroy()
        def frames(no):
            if no == 1:
                clear()
                buttons()
                last_pages(self, 1)
            elif no == 2:
                clear()
                buttons()
                last_pages(self, 2)
            elif no == 3:
                clear()
                buttons()
                last_pages(self, 3)
            elif no == 4:
                clear()
                buttons()
                last_pages(self, 4)
            elif no == 5:
                clear()
                buttons()
                last_pages(self, 5)
        buttons()
        frames(1)

def last_pages(self, flg):
    if flg == 1:
        heading = Label(self, text="List of Books", fg="white", bg="black", font=("bold", 20))
        heading.place(x=320, y=50)
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial Bold', 10))
        tree_frame = Frame(self)
        tree_frame.place(x=200, y=160)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        my_tree = ttk.Treeview(tree_frame, height=20, yscrollcommand=tree_scroll.set)
        my_tree.pack()
        tree_scroll.config(command=my_tree.yview)
        my_tree['columns'] = ("ID", "Name", "Author", "Quantity")
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Name", anchor=W, width=180)
        my_tree.column("Author", anchor=W, width=150)
        my_tree.column("Quantity", anchor=W, width=50)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Name", text="Book Name", anchor=W)
        my_tree.heading("Author", text="Author Name", anchor=W)
        my_tree.heading("Quantity", text="Quantity", anchor=W)
        def search(s):
            my_c = my_db.cursor()
            if s == 0:
                for books in my_tree.get_children():
                    my_tree.delete(books)
                my_c.execute("SELECT * FROM books")
                for books in my_c:
                    my_tree.insert(parent='', index='end', iid=0, values=books)
            elif s == 1:
                if self.search.get() != "":
                    for books in my_tree.get_children():
                        my_tree.delete(books)
                my_c.execute("SELECT * FROM books WHERE Book_Name=%s", (self.search.get(),))
                for books in my_c:
                    my_tree.insert(parent='', index='end', iid=0, values=books)
        search(0)
        self.search = Entry(self, width=50)
        self.search.place(x=250, y=104)
        arrow_button = Button(self, text="<", font=20, command=lambda s=0: search(s))
        arrow_button.place(x=210, y=100)
        search_button = Button(self, text="search", font=20, command=lambda s=1: search(s))
        search_button.place(x=570, y=100)
        self.bind('<Return>', lambda event: search(1))
    elif flg == 2:
        heading = Label(self, text="Add Books", fg="white", bg="black", font=("bold", 20))
        heading.place(x=300, y=50)
        book_name = Label(self, text="Enter Book Name:", fg="black", bg="grey", font=15)
        book_name.place(x=240, y=238)
        self.book_name = Entry(self)
        self.book_name.place(x=400, y=240)
        book_author = Label(self, text="Enter Author Name:", fg="black", bg="grey", font=15)
        book_author.place(x=240, y=280)
        self.book_author = Entry(self)
        self.book_author.place(x=400, y=282)
        quantity = Label(self, text="Quantity:", fg="black", bg="grey", font=15)
        quantity.place(x=240, y=320)
        self.quantity = Entry(self)
        self.quantity.place(x=400, y=319)
        def state():
            while True:
                if self.book_name.get() == "" or self.book_author.get() == "" or self.quantity.get() == "":
                    submit_button['state'] = DISABLED
                else:
                    submit_button['state'] = NORMAL
                    break
        def add_book():
            if int(self.quantity.get()) <= 0:
                msg.showerror("System error", "Give Valid Quantity!")
                self.focus_force()
            else:
                c = my_db.cursor()
                c.execute("Insert into books values(NULL, %s, %s, %s)", (self.book_name.get(), self.book_author.get(), self.quantity.get()))
                my_db.commit()
                self.destroy()
                threading.Thread(target=speak("Book added successfully to the record!"))
                msg.showinfo("notification", "Book added successfully to the record!")
        submit_button = Button(self, text="Submit", font=20, command=add_book)
        submit_button.place(x=600, y=540)
        self.bind('<Return>', lambda event: add_book())
        threading.Thread(target=state).start()
    elif flg == 3:
        heading = Label(self, text="Delete Books", fg="white", bg="black", font=("bold", 20))
        heading.place(x=300, y=50)
        book_name = Label(self, text="Enter Book Name:", fg="black", bg="grey", font=15)
        book_name.place(x=240, y=238)
        self.book_name = Entry(self)
        self.book_name.place(x=400, y=240)
        book_author = Label(self, text="Enter Author Name:", fg="black", bg="grey", font=15)
        book_author.place(x=240, y=280)
        self.book_author = Entry(self)
        self.book_author.place(x=400, y=282)
        def state():
            while True:
                if self.book_name.get() == "" or self.book_author.get() == "":
                    delete_button['state'] = DISABLED
                else:
                    delete_button['state'] = NORMAL
                    break
        def delete_book():
            c = my_db.cursor()
            c.execute("select Quantity from books where Book_Name=%s and Author_Name=%s", (self.book_name.get(), self.book_author.get()))
            q = 0
            for i in c:
                q = int(i[0])
            if q >= 0:
                c.execute("DELETE from books where Book_Name=%s and Author_Name=%s", (self.book_name.get(), self.book_author.get()))
                my_db.commit()
                self.destroy()
                threading.Thread(target=speak("Book is Deleted from the record!"))
                msg.showinfo("notification", "Book is Deleted from the record!")
                self.focus_force()
            else:
                msg.showerror("error", "Enter valid Book Information")
                self.focus_force()
        delete_button = Button(self, text="Submit", font=20, command=delete_book)
        delete_button.place(x=600, y=540)
        self.bind('<Return>', lambda event: delete_book())
        threading.Thread(target=state).start()
    elif flg == 4:
        heading = Label(self, text="Issue Books", fg="white", bg="black", font=("bold", 20))
        heading.place(x=300, y=50)
        book_name = Label(self, text="Enter Book Name:", fg="black", bg="grey", font=15)
        book_name.place(x=240, y=238)
        self.book_name = Entry(self)
        self.book_name.place(x=400, y=240)
        book_author = Label(self, text="Enter Author Name:", fg="black", bg="grey", font=15)
        book_author.place(x=240, y=280)
        self.book_author = Entry(self)
        self.book_author.place(x=400, y=282)
        def state():
            while True:
                if self.book_name.get() == "" or self.book_author.get() == "":
                    issue_button['state'] = DISABLED
                else:
                    issue_button['state'] = NORMAL
                    break
        def issue_book():
            c = my_db.cursor()
            c.execute("select Quantity from books where Book_Name=%s and Author_Name=%s", (self.book_name.get(), self.book_author.get()))
            q = 0
            for a in c:
                q = int(a[0])
            if q >= 1:
                q -= 1
                c.execute("update books set Quantity=%s where Book_Name=%s and Author_Name=%s", (q, self.book_name.get(), self.book_author.get()))
                my_db.commit()
                current[4] = self.book_name.get()
                current[5] = self.book_author.get()
                send_time = datetime.datetime.now()
                return_time = send_time + datetime.timedelta(days=10)
                send_time = send_time.strftime("%d-%m-%Y %H:%M:%S")
                return_time = return_time.strftime("%d-%m-%Y")
                c.execute("select Member_ID from members where Member_Name=%s and Email_Id=%s", (current[1], current[2]))
                idd = 0
                for i in c:
                    idd = int(i[0])
                c.execute("insert into issued values(NULL, %s, %s, %s, %s, %s, %s)", (idd, self.book_name.get(), self.book_author.get(), send_time, return_time, 0))
                my_db.commit()
                send_email(send_time, return_time)
                self.destroy()
                threading.Thread(target=speak(f"book is issued by {current[1]}"))
                msg.showinfo("notification", "Book is Available \nBook is issued successfully!")
                self.focus_force()
            else:
                msg.showerror("error", "Either Book is unavailable or you have entered wrong information!")
                self.focus_force()
        issue_button = Button(self, text="Submit", font=20, command=issue_book)
        issue_button.place(x=600, y=540)
        self.bind('<Return>', lambda event: issue_book())
        threading.Thread(target=state).start()
    elif flg == 5:
        heading = Label(self, text="Return Books", fg="white", bg="black", font=("bold", 20))
        heading.place(x=300, y=50)
        book_list = Label(self, text="List of your Issued Books:", fg="white", bg="black", font=15)
        book_list.place(x=140, y=290)
        book_name = Label(self, text="Enter Book Name:", fg="black", bg="grey", font=15)
        book_name.place(x=240, y=163)
        self.book_name = Entry(self)
        self.book_name.place(x=400, y=165)
        book_author = Label(self, text="Enter Author Name:", fg="black", bg="grey", font=15)
        book_author.place(x=240, y=205)
        self.book_author = Entry(self)
        self.book_author.place(x=400, y=207)
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial Bold', 10))
        tree_frame = Frame(self)
        tree_frame.place(x=140, y=320)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        my_tree = ttk.Treeview(tree_frame, height=8, yscrollcommand=tree_scroll.set)
        my_tree.pack()
        tree_scroll.config(command=my_tree.yview)
        my_tree['columns'] = ("Name", "Author", "Issued", "Return")
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Name", anchor=W, width=120)
        my_tree.column("Author", anchor=W, width=120)
        my_tree.column("Issued", anchor=W, width=120)
        my_tree.column("Return", anchor=W, width=120)
        my_tree.heading("Name", text="Book Name", anchor=W)
        my_tree.heading("Author", text="Author Name", anchor=W)
        my_tree.heading("Issued", text="Issued Date", anchor=W)
        my_tree.heading("Return", text="Return Date", anchor=W)
        c = my_db.cursor()
        c.execute("SELECT issued.Book_Name, issued.Author_Name, issued.Issued_Date, issued.Return_Date FROM members INNER JOIN issued ON members.Member_ID=issued.Member_ID WHERE members.Email_Id=%s", (current[2],))
        for books in c:
            my_tree.insert(parent='', index='end', iid=0, values=books)
        def state():
            while True:
                if self.book_name.get() == "" or self.book_author.get() == "":
                    return_button['state'] = DISABLED
                else:
                    return_button['state'] = NORMAL
                    break
        def return_book():
            c.execute("select Quantity from books where Book_Name=%s and Author_Name=%s", (self.book_name.get(), self.book_author.get()))
            q = 0
            for b in c:
                q = int(b[0])
            if q >= 0:
                q += 1
                try:
                    c.execute("SELECT Member_ID from members where Email_Id=%s", (current[2],))
                    m_id = 0
                    for a in c:
                        m_id = int(a[0])
                    c.execute("DELETE from issued where Book_Name=%s and Member_ID=%s", (self.book_name.get(), m_id))
                    my_db.commit()
                    c.execute("update books set Quantity=%s where Book_Name=%s and Author_Name=%s", (q, self.book_name.get(), self.book_author.get()))
                    my_db.commit()
                    self.destroy()
                    msg.showinfo("notification", "Book is return successfully!")
                    threading.Thread(target=speak(f"book is return by {current[1]}"))
                    self.focus_force()
                except Exception:
                    self.focus_force()
            else:
                msg.showerror("error", "You have entered wrong information!")
                self.focus_force()
        return_button = Button(self, text="Submit", font=20, command=return_book)
        return_button.place(x=600, y=540)
        self.bind('<Return>', lambda event: return_book())
        threading.Thread(target=state).start()

def send_email(send_time, return_time):
    sender_email = 'digi.lib.system@gmail.com'
    receiver_email = current[2]
    email_password = 'Library@0'
    subject = "Regarding issued book from central library"
    text = f"""
    Hello {current[1]}, 
    You have recently issued a book from central library!
    \nBook Details:
    \tBook Name- {current[4]}
    \tAuthor Name- {current[5]}
    \tIssued by- {current[1]}
    \tDate of Issue- {send_time}
    \tExpected Return Date- {return_time}
    """
    message = 'Subject: {}\n\n{}'.format(subject, text)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, email_password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()
    print('email sent')

def reminder_email():
    now = datetime.datetime.now()
    flag[1] = 1
    try:
        c = my_db.cursor()
        c.execute("SELECT members.Email_Id, members.Member_Name, issued.Book_Name, issued.Author_Name, issued.Issued_Date, issued.Return_Date, issued.Flag FROM members INNER JOIN issued ON members.Member_ID=issued.Member_ID")
        for i in c:
            email = i[0]
            name = i[1]
            book_name = i[2]
            author_name = i[3]
            issued_date = i[4]
            return_date = i[5]
            re_date = datetime.datetime.strptime(i[5], "%d-%m-%Y")
            flg = i[6]
            reminder_date = re_date - datetime.timedelta(days=1)
            recommendation_date = re_date - datetime.timedelta(days=5)
            if (now >= reminder_date) and (flg < 2):
                sender_email = 'digi.lib.system@gmail.com'
                receiver_email = email
                email_password = 'Library@0'
                subject = "Reminder message from central library"
                text = f"""
                Hello {name}, 
                You have to return the book tomorrow.
                Book Details:
                \tBook Name- {book_name}
                \tAuthor Name- {author_name}
                \tIssued by- {name}
                \tDate of Issue- {issued_date}
                \tExpected Return Date- {return_date}
                """
                message = 'Subject: {}\n\n{}'.format(subject, text)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, email_password)
                server.sendmail(sender_email, receiver_email, message)
                server.quit()
                print('reminder email sent')
                c.execute("UPDATE issued SET Flag=%s where Issued_Date=%s and Return_date=%s", (2, issued_date, return_date))
                my_db.commit()
            elif (now >= recommendation_date) and (flg < 1):
                sender_email = 'digi.lib.system@gmail.com'
                receiver_email = email
                email_password = 'Library@0'
                c.execute("SELECT Book_Name, Author_Name FROM books WHERE Author_Name=%s", (author_name,))
                book = ""
                author = ""
                for books in c:
                    book, author = books
                subject = "Recommendation for you"
                text = f"""
                Hello {name}, 
                More Books from the Author {author_name} -
                \n\n{"{:<20} {:<20}".format('Book Name', 'Author Name')}
                \n{"{:<20} {:<20}".format(book, author)}
                """
                message = 'Subject: {}\n\n{}'.format(subject, text)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, email_password)
                server.sendmail(sender_email, receiver_email, message)
                server.quit()
                print('recommendation email sent')
                c.execute("update issued set Flag=%s where Issued_Date=%s and Return_date=%s", (1, issued_date, return_date))
                my_db.commit()
    except Exception:
        pass

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    engine.say(audio)
    engine.runAndWait()

def take_command():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        rec.energy_threshold = 4000
        audio = rec.listen(source)
    try:
        command = rec.recognize_google(audio, language='en-in')
        print(f">>>{command}\n")
    except Exception:
        return ""
    return command

def main():
    while True:
        command = take_command().lower()
        now = int(datetime.datetime.now().minute)
        if current[0] == "exit":
            break
        if (now % 2 == 0) and (flag[1] == 0):
            threading.Thread(target=reminder_email).start()
        elif now % 2 != 0:
            flag[1] = 0
        if "student" in command:
            threading.Thread(target=lambda: middle_pages(1)).start()
        elif ("librarian" in command) or ("library" in command):
            threading.Thread(target=lambda: middle_pages(2)).start()
        elif "registration" in command:
            threading.Thread(target=lambda: middle_pages(3)).start()
        elif "list of books" in command:
            threading.Thread(target=lambda: middle_pages(7)).start()
        elif "add book" in command:
            threading.Thread(target=lambda: middle_pages(8)).start()
        elif "delete book" in command:
            threading.Thread(target=lambda: middle_pages(9)).start()
        elif "issue book" in command:
            threading.Thread(target=lambda: middle_pages(10)).start()
        elif "return book" in command:
            threading.Thread(target=lambda: middle_pages(11)).start()
        elif "back" in command:
            keyboard.press_and_release('escape')
        elif "exit" in command:
            keyboard.press_and_release('escape')
            break
        elif ("next" or "search" or "submit") in command:
            keyboard.press_and_release('enter')

threading.Thread(target=main).start()
threading.Thread(target=first_page).start()
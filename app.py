from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta

from functions import filters, create_footer, create_scrollable_frame, flush, edit_atr, index_converter
from functions import create_search_bar, create_menu, get_image, show_items, recommend_events, code_converter
from classes import Ticket, Account, Event
from sql import SQL

class App:
    def __init__(self):

        self.sql = SQL()

        self.root = Tk()
        self.root.title("Event Organizer")
        self.root.geometry("908x700")
        self.root.geometry("{0}x{1}+-8+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight() - 80))

        self.logged_in = False
        self.curr_account : Account = None
        self.user_preference = []

        self.filter_var = StringVar(value = "All Events")
        self.sort_by_var = StringVar(value = "Name")
        self.order = StringVar(value = "Ascending")
        self.get_recommendation = BooleanVar(value=1)

        self.scrollable_frame = None
        self.get_database()
        self.homepage()
        self.root.mainloop()

    def get_database(self):
        def generate_unique_code(prefix, starting_number=1):
            while True:
                code = prefix + str(starting_number).zfill(3)
                yield code
                starting_number += 1

        self.events: dict = {}
        self.event_attributes : dict = {}
        self.accounts: dict = {}
        self.tickets: dict = {}

        self.account_preferences_matrix = list()
        for account_id, first_name, last_name, username, password, email, wallet in self.sql.select_all("account"):
            self.accounts[username] = Account(account_id, first_name, last_name, username, password, email, wallet)
            self.account_preferences_matrix.append([0 for i in range(7)])
        self.acc_generator = generate_unique_code("A", int(account_id[1:]) + 1)
        
        self.event_attributes_matrix = list(self.sql.select_attributes())
        for event_id, event_name, schedule, events_detail, price, event_photo, status, genre in self.sql.select_all("event"):
            self.events[event_id] = Event(event_id, event_name, price, events_detail, event_photo, schedule, status, genre)
            self.event_attributes[event_id] = self.sql.select_attribute(event_id)
        self.ev_generator = generate_unique_code("E", int(event_id[1:]) + 1)

        for ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id, event_name, price, detail, event_photo, schedule, status, genre, quantity in self.sql.select_all_ticket():
            self.tickets[ticket_id] = Ticket(ticket_id, account_id, first_name, last_name, username, password, email,wallet, event_id, event_name, price, detail, event_photo, schedule, status, genre, quantity)
            edit_atr(self.account_preferences_matrix[index_converter(self,username)], self.event_attributes[event_id], "add")
        self.tic_generator = generate_unique_code("T", int(ticket_id[1:]) + 1)

        
    def homepage(self, data: list[Ticket] = None, recommending = True):
        if data == None:
            data = self.events.values()
            data = filters(data, self.filter_var.get(), None, self.sort_by_var.get(), self.order.get())

        flush(self)
        create_scrollable_frame(self)
        create_menu(self, self.scrollable_frame)
        create_search_bar(self, "item")
        self.sql.update_all_events_state()
        
        label_frame = Frame(self.scrollable_frame)
        label_frame.pack(fill="x", pady=10, anchor="n")

        refresh_label = Label(label_frame, fg="white", font=("Arial", 12), cursor="hand2")
        refresh_label.bind("<Button-1>", lambda e: self.homepage())
        icon_image = get_image(rf"imgs/refresh.png", 20, 20)
        refresh_label.config(image=icon_image)
        refresh_label.image = icon_image
        refresh_label.pack(side="right", padx=10, pady=10)

        filter_frame = Frame(label_frame)
        filter_frame.pack(side="right", padx=10)
        Label(filter_frame, text= "Filter by",font=("Arial", 12)).pack()
        filter_menu = OptionMenu(filter_frame, self.filter_var, "All Events", "Passed Events", "Coming Soon", command=lambda e: self.homepage(filters(self.events.values(),self.filter_var.get(),None, self.sort_by_var.get(), self.order.get())))
        filter_menu.pack()
        
        sort_frame = Frame(label_frame)
        sort_frame.pack(side="right", padx=10)
        Label(sort_frame, text= "Order by",font=("Arial", 12)).pack()
        sort_by_menu = OptionMenu(sort_frame, self.sort_by_var, "Name", "Genre", "Price", "Schedule", command=lambda e: self.homepage(filters(self.events.values(), self.filter_var.get(),None, self.sort_by_var.get(), self.order.get())))
        sort_by_menu.pack(padx = 10)

        order_frame = Frame(label_frame)
        order_frame.pack(side="right", padx=10)
        Label(order_frame, text= "Ordering",font=("Arial", 12)).pack()
        order = OptionMenu(order_frame, self.order, "Ascending", "Descending", command=lambda e: self.homepage(filters(self.events.values(), self.filter_var.get(),None, self.sort_by_var.get(), self.order.get())))
        order.pack(padx = 10)

        if self.logged_in:
            check = Checkbutton(label_frame, text="Get Recommendation", variable=self.get_recommendation, command= self.homepage)
            check.pack(side = "right", padx = 10, pady = 10)
        
        if self.get_recommendation.get() and self.logged_in and recommending:
            recommendations = [self.events[code_converter(self, index)] for index in recommend_events(self, self.user_preference, self.event_attributes_matrix) if self.events[code_converter(self, index)].status != "passed"]

            if recommendations:
                Label(label_frame, text = "Showing recommendations:",font=("Arial", 16, "bold"), anchor="w", justify="left").pack(side = "left")
                show_items(self, recommendations, "item", True)
            else:
                Label(label_frame, text = "No available recommendations",font=("Arial", 16, "bold"), anchor="w", justify="left").pack(side = "left")
                
            currently_event = Label(self.scrollable_frame, text=f"Currently available events :", font=("Arial", 16, "bold"), anchor="w", justify="left")
            currently_event.pack(side="top", padx=10, fill = "x")
        else:
            currently_event = Label(label_frame, text=f"Currently available events :", font=("Arial", 16, "bold"), anchor="w", justify="left")
            currently_event.pack(side="left", padx=10, fill="x")

        show_items(self, data, "item")
        create_footer(self.scrollable_frame)

    def create_account_window(self):
        def register_account(first_name_entry:Entry, last_name_entry:Entry, username_entry:Entry, password_entry:Entry, email_entry:Entry):
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            email = email_entry.get()
            wallet = 0

            if not first_name or not last_name or not username or not password or not email:
                messagebox.showwarning("Input Error", "Please fill all fields")
            else:
                id = next(self.acc_generator)
                self.sql.add_account(id, first_name, last_name, username, password, email, wallet)
                self.accounts[username] = Account(id, first_name, last_name, username, password, email, wallet)
                self.account_preferences_matrix.append([0, 0, 0, 0, 0, 0, 0])
                messagebox.showinfo("Creation Status", f"Account creation success, you can login as {username} now")
                self.homepage()

        flush(self)
        create_scrollable_frame(self,)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.scrollable_frame, text="CREATE A NEW ACCOUNT", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        Label(self.scrollable_frame, text="First Name", font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=5)
        first_name_entry = Entry(self.scrollable_frame, width=30)
        first_name_entry.grid(row=1, column=1, pady=5)

        Label(self.scrollable_frame, text="Last Name", font=("Arial", 12)).grid(row=2, column=0, sticky='w', pady=5)
        last_name_entry = Entry(self.scrollable_frame, width=30)
        last_name_entry.grid(row=2, column=1, pady=5)

        Label(self.scrollable_frame, text="Username", font=("Arial", 12)).grid(row=3, column=0, sticky='w', pady=5)
        username_entry = Entry(self.scrollable_frame, width=30)
        username_entry.grid(row=3, column=1, pady=5)

        Label(self.scrollable_frame, text="Password", font=("Arial", 12)).grid(row=4, column=0, sticky='w', pady=5)
        password_entry = Entry(self.scrollable_frame, width=30)
        password_entry.grid(row=4, column=1, pady=5)

        Label(self.scrollable_frame, text="Email", font=("Arial", 12)).grid(row=5, column=0, sticky='w', pady=5)
        email_entry = Entry(self.scrollable_frame, width=30)
        email_entry.grid(row=5, column=1, pady=5)

        Button(self.scrollable_frame, text="CREATE ACCOUNT", font=("Arial", 10),command=lambda: register_account(first_name_entry, last_name_entry,username_entry, password_entry, email_entry), bg="#2c3e50", fg="white", width=15).grid(row=7, column=1, pady=15, sticky='e')

        cancel_link = Label(self.scrollable_frame, text="CANCEL", font=("Arial", 10), fg="#2c3e50", cursor="hand2")
        cancel_link.grid(row=7, column=0, pady=15, sticky='w')
        cancel_link.bind("<Button-1>", lambda e: self.homepage())  

    def show_login_page(self):
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            if username == "" and password == "":
                status_label.config(text="Please enter registered username and password", font=('Arial', 10))
            elif username not in self.accounts:
                status_label.config(text="Please enter registered username", font=('Arial', 10))
            elif password != self.accounts[username].password:
                status_label.config(text="Please enter correct password", font=('Arial', 10))
            else:
                status_label.config(text=f"Succesfully logged in as {username}.", font=('Arial', 10))
                self.curr_account = self.accounts[username]
                self.user_preference = [self.account_preferences_matrix[index_converter(self, username)]]
                self.logged_in = True
                self.root.after(500, self.homepage)

        flush(self)
        create_scrollable_frame(self)

        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        title_label = Label(self.scrollable_frame, text="LOGIN TO YOUR ACCOUNT", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        Label(self.scrollable_frame, text="Username", font=("Arial", 12)).grid(row=1, column=0, sticky='w', padx=(0, 10))
        username_entry = Entry(self.scrollable_frame, width=30)
        username_entry.grid(row=1, column=1, pady=5)

        Label(self.scrollable_frame, text="Password", font=("Arial", 12)).grid(row=2, column=0, sticky='w', padx=(0, 10))
        password_entry = Entry(self.scrollable_frame, width=30, show="*")
        password_entry.grid(row=2, column=1, pady=5)

        Button(self.scrollable_frame, text="LOGIN", font=("Arial", 10), command=login, bg="#2c3e50",fg="white", width=15).grid(row=3, column=0, columnspan=2, pady=15, sticky='ew')

        status_label = Label(self.scrollable_frame, text="", fg="red")
        status_label.grid(row=4, column=0, columnspan=2)

        cancel_link = Label(self.scrollable_frame, text="CANCEL", font=("Arial", 10), fg="#2c3e50", cursor="hand2")
        cancel_link.grid(row=5, column=0, pady=5, sticky='w')
        cancel_link.bind("<Button-1>", lambda e: self.homepage())

        create_account_link = Label(self.scrollable_frame, text="CREATE A NEW ACCOUNT", font=("Arial", 10), fg="#2c3e50", cursor="hand2")
        create_account_link.grid(row=5, column=1, pady=5, sticky='e')
        create_account_link.bind("<Button-1>", lambda e: self.create_account_window())

    def show_profile(self):
        def update_profile(account_id, first_name, last_name, username, password, email, datas_before):
            self.sql.save_updated_profile(account_id, first_name, last_name, username, password, email)
            self.curr_account.first_name = first_name
            self.curr_account.last_name = last_name
            self.curr_account.username = username
            self.curr_account.password = password 
            self.curr_account.email = email

            del self.accounts[datas_before[3]]
            self.accounts[username] = self.curr_account

            messagebox.showinfo("Notice", "Successfully updated your profile!")

        flush(self)
        create_menu(self, self.root)
        create_search_bar(self, "profile")

        create_scrollable_frame(self)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.scrollable_frame, text="USER PROFILE", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        entries = {}
        
        datas_before = [self.curr_account.account_id, self.curr_account.first_name, self.curr_account.last_name, self.curr_account.username, self.curr_account.password, self.curr_account.email]
        for idx, title in enumerate(["First Name", "Last Name", "Username", "Password", "Email"], start=1):
            Label(self.scrollable_frame, text=title, font=("Arial", 12)).grid(row = idx, column = 0, pady=5)
            
            entry = Entry(self.scrollable_frame, width=40)
            entry.insert(0, datas_before[idx - 1])
            entry.grid(row= idx, column=1, pady=5)
            entries[title] = entry

        save_button = Button(self.scrollable_frame, text="SAVE CHANGES", font=("Arial", 10),
            command=lambda: update_profile(self.curr_account.account_id,entries["First Name"].get(), entries["Last Name"].get(),entries["Username"].get(), entries["Password"].get(),entries["Email"].get(), datas_before),
            bg="#2c3e50", fg="white", width=20)
        save_button.grid(row=6, column=0, columnspan=2, pady=15)

    def show_cart(self, data : list[Ticket] = None):
        if data == None: 
            data = [Ticket(ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id,event_name, price, detail, event_photo, schedule, status, genre, quantity) for ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id, event_name, price, detail, event_photo, schedule, status,genre, quantity in self.sql.select_ticket(self.curr_account.account_id)]

        flush(self)

        create_scrollable_frame(self)
        create_menu(self, self.scrollable_frame)
        create_search_bar(self,"tickets")

        Label(self.scrollable_frame, text=f"Welcome {self.curr_account.last_name}, {self.curr_account.first_name} !",font=("Arial", 16, "bold"), anchor="w", justify="right").pack()
        Label(self.scrollable_frame, text=f"Showing your tickets : ", font=("Arial", 10), anchor="w",justify="right").pack()
        
        show_items(self, data, "ticket")
        create_footer(self.scrollable_frame)

    def buy(self, item : Ticket):
        self.show_event(item)

        def buy_ticket(item: Ticket):
            if self.curr_account is None:
                messagebox.showwarning("Not logged in", "Please log in before buying.")
                return

            self.user_payment(item)

        def decrease_quantity():
            if self.quantity > 1:
                self.quantity -= 1
                curr_price = self.quantity * item.price
                total_price.config(text=f"total price :      $ {curr_price}")
            else:
                messagebox.showinfo("Notice", "Quantity cannot be less than 1!")
            quantity_label.config(text=self.quantity)

        def increase_quantity():
            tickets_for_event = self.sql.get_ticket_id(self.curr_account.account_id, item.event_id)
            if 5 - len(tickets_for_event) - self.quantity == 0:
                amount_ticket = f"{self.quantity} tickets" if self.quantity > 1 else "1 ticket"
                messagebox.showinfo("Notice", f"You can only buy {amount_ticket}!")

            else:  
                self.quantity += 1
                curr_price = self.quantity * item.price
                total_price.config(text=f"total price :      $ {curr_price}")

            quantity_label.config(text=self.quantity)

        self.sql.update_all_events_state()

        if item.status == "passed":
            text_frame = Frame(self.left_frame)
            text_frame.pack(fill="both", expand=True, padx=10, pady=10)
            Label(text_frame, text=f"The Event Has Passed", font=("Arial", 14, "bold")).pack()

        else:
            if self.curr_account == None:
                Label(self.left_frame, text="Login to buy ticket ", font=("Arial", 13, "bold")).pack(expand=True, )
                return
            
            tickets_for_event = self.sql.get_ticket_id(self.curr_account.account_id, item.event_id)
            if len(tickets_for_event) < 5: # [('T005',)]
                self.quantity = 1
                curr_price = self.quantity * item.price

                quantity_frame = Frame(self.left_frame, padx=100)
                quantity_frame.pack(fill="x", expand=True)

                Label(self.left_frame, text="Quantity : ", font=("Arial", 10)).pack()

                minus_button = Button(quantity_frame, text="-", command=decrease_quantity, width=2)
                minus_button.pack(side="left", fill="y")

                quantity_label = Label(quantity_frame, text=self.quantity, relief="sunken")

                quantity_label.pack(side="left", fill="both", expand=True)

                add_button = Button(quantity_frame, text="+", command=increase_quantity, width=2)
                add_button.pack(side="left", fill="y")

                buy_button = Button(self.left_frame, text="Buy Ticket", command=lambda: buy_ticket(item), bg="#2c3e50", fg="white", width=25, height=2)
                buy_button.pack(side="top", anchor="n")

                total_price = Label(self.left_frame, text=f"total price :      $ {curr_price}", font=("Arial", 10), anchor="n")
                total_price.pack(side="top", fill="both", expand=True)

            else:
                text_frame = Frame(self.left_frame)
                text_frame.pack(fill="both", expand=True, padx=10, pady=10)

                Label(text_frame, text=f"You Can Only Buy 5 Tickets", font=("Arial", 14, "bold")).pack()
                Label(text_frame, text=f"For This Concert", font=("Arial", 14, "bold")).pack()

    def show_event(self, item: Ticket):

        flush(self)
        create_menu(self, self.root)

        main_frame = Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        self.left_frame = Frame(main_frame, width=700)
        self.left_frame.pack(side="left", fill="both", padx=10, pady=10)

        right_frame = Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        img_frame = Frame(self.left_frame,  bg="#2c3e50", relief=RAISED)
        img_frame.pack(fill="both", expand=True, padx=10, pady=10)

        icon_image = get_image(item.event_photo, 400, 400)
        image_frame = Label(img_frame, image=icon_image, width=400, height=400)
        image_frame.image = icon_image
        image_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10, anchor="n")

        details_frame = Frame(right_frame, bg="white")
        details_frame.pack(fill="x", padx=20, pady=10)

        orchestra_label = Label(details_frame, text=item.event_name, font=("Arial", 14, "bold"), fg="#34495e", bg="white", justify="left")
        orchestra_label.grid(row=0, column=0, sticky="w", padx=5)

        conductor_label = Label(details_frame, text=item.schedule, font=("Arial", 12, "bold"), fg="#34495e", bg="white", justify="left")
        conductor_label.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 0))

        program_label = Label(details_frame, text="$" + str(item.price), font=("Arial", 12), fg="#1a1a1a", bg="white", justify="left")
        program_label.grid(row=2, column=0, sticky="w", padx=5, pady=(10, 0))

        description_frame = Frame(right_frame, bg="white")
        description_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        canvas = Canvas(description_frame, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(description_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        content_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        description_label = Label(content_frame, text=item.detail, font=("Arial", 11), fg="#1a1a1a", bg="white", wraplength=500, justify="left")
        description_label.pack(fill="x", padx=5, pady=(0, 10))

        create_footer( self.root)

    def user_payment(self, item : Ticket):
        
        def update_countdown(label : Label, end_time):
            now = datetime.now()
            remaining_time = end_time - now
        
            if remaining_time.total_seconds() > 0:
                hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                label.config(text="Pay Before " + time_str, font=("Arial", 14), fg="blue")
                label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
                label.after(1000, update_countdown, label, end_time)
            else:
                label.config(text="Your payment is passed the time limit!", fg="red", font=("Arial", 14))
                label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
                messagebox.showwarning("Payment failed", "Your payment is failed!")
                self.homepage()
        
        def do_payment():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            amount = amount_entry.get()
            selected_payment = payment_method.get()
            total_price = str(self.quantity * float(item.price))

            if not first_name or not last_name or not email or not phone or not amount:
                messagebox.showwarning("Input Error", "Please fill all fields")
            elif amount != total_price:
                messagebox.showwarning("Invalid Amount", "Please fill the correct amount")
                return
            else:
                if selected_payment == "Wallet" and self.curr_account.wallet < float(total_price):
                    messagebox.showwarning("Insufficient Funds", "Your wallet balance is insufficient to complete the payment.")
                else:
                    if selected_payment == "Wallet":
                        self.curr_account.wallet = float(self.curr_account.wallet) - float(total_price)
                        self.sql.update_data("account", self.curr_account.account_id, "wallet", self.curr_account.wallet)
                        edit_atr(self.user_preference[0], self.event_attributes[item.event_id], "add")
                    
                    for ticket in range(self.quantity):
                        ticket_id = next(self.tic_generator)
                        account_id = self.curr_account.account_id
                        event_id = item.event_id
                        quantity = self.quantity
                
                        self.sql.add_ticket(ticket_id, account_id, event_id, quantity)
                        self.tickets[ticket_id] = Ticket(ticket_id, self.curr_account.account_id, self.curr_account.first_name,self.curr_account.last_name, self.curr_account.username,self.curr_account.password, self.curr_account.email,self.curr_account.wallet, item.event_id, item.event_name, item.price,item.detail, item.event_photo, item.schedule, item.status, item.genre, quantity)
            
                    messagebox.showinfo("Notice", f"Succesfully purchased {quantity} tickets for ${total_price}")
                    self.homepage()
            return
    
        flush(self)
        
        main_frame = Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        countdown_label = Label(main_frame, text="", font=("Arial", 24))
        countdown_label.pack(pady=20)
        end_time = datetime.now() + timedelta(minutes=1)
        
        update_countdown(countdown_label, end_time)

        blank_label = Label(main_frame, text="", font=("Arial", 18))
        blank_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        title_label = Label(main_frame, text="USER PAYMENT", font=("Arial", 16, "bold"))
        title_label.grid(row=2, column=0, columnspan=2, pady=(0, 15))

        first_name_label = Label(main_frame, text="First Name", font=("Arial", 12))
        first_name_label.grid(row=3, column=0, sticky='w', pady=5)
        first_name_entry = Entry(main_frame, width=40)
        first_name_entry.grid(row=3, column=1, pady=5)

        last_name_label = Label(main_frame, text="Last Name", font=("Arial", 12))
        last_name_label.grid(row=4, column=0, sticky='w', pady=5)
        last_name_entry = Entry(main_frame, width=40)
        last_name_entry.grid(row=4, column=1, pady=5)

        email_label = Label(main_frame, text="Email", font=("Arial", 12))
        email_label.grid(row=5, column=0, sticky='w', pady=5)
        email_entry = Entry(main_frame, width=40)
        email_entry.grid(row=5, column=1, pady=5)

        phone_label = Label(main_frame, text="Phone", font=("Arial", 12))
        phone_label.grid(row=6, column=0, sticky='w', pady=5)
        phone_entry = Entry(main_frame, width=40)
        phone_entry.grid(row=6, column=1, pady=5)

        total_price = str(self.quantity * float(item.price))
        amount_label = Label(main_frame, text="Price to Pay ($)", font=("Arial", 12))
        amount_label.grid(row=7, column=0, sticky='w', pady=5)
        amount_entry = Entry(main_frame, width=40)
        amount_entry.insert(0, total_price)
        amount_entry.grid(row=7, column=1, pady=5)

        Label(main_frame, text="Payment Method:", font=("Arial", 12)).grid(row=8, column=0, sticky='w', pady=5)
        payment_method = StringVar()
        payment_method.set("Wallet")  
        payment_options = ["Wallet", "Credit Card", "Debit Card", "PayPal", "Bank Transfer"]
        payment_dropdown = OptionMenu(main_frame, payment_method, *payment_options)
        payment_dropdown.grid(row=8, column=1, pady=5)

        submit_button = Button(main_frame, text="Submit Payment", font=("Arial", 12),command=do_payment, bg="#2c3e50", fg="white", width=20)
        submit_button.grid(row=9, column=0, columnspan=2, pady=15)

        cancel_label = Label(main_frame, text="CANCEL", font=("Arial", 10), fg="#2c3e50", cursor="hand2")
        cancel_label.grid(row=10, column=0, columnspan=2, pady=15)
        cancel_label.bind("<Button-1>", lambda e: self.homepage())

    def show_event(self, item: Ticket):

        flush(self)
        create_menu(self, self.root)

        main_frame = Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        self.left_frame = Frame(main_frame, width=700)
        self.left_frame.pack(side="left", fill="both", padx=10, pady=10)

        right_frame = Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        img_frame = Frame(self.left_frame,  bg="#2c3e50", relief=RAISED)
        img_frame.pack(fill="both", expand=True, padx=10, pady=10)

        icon_image = get_image(item.event_photo, 400, 400)
        image_frame = Label(img_frame, image=icon_image, width=400, height=400)
        image_frame.image = icon_image
        image_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10, anchor="n")

        details_frame = Frame(right_frame, bg="white")
        details_frame.pack(fill="x", padx=20, pady=10)

        orchestra_label = Label(details_frame, text=item.event_name, font=("Arial", 14, "bold"), fg="#34495e", bg="white", justify="left")
        orchestra_label.grid(row=0, column=0, sticky="w", padx=5)

        conductor_label = Label(details_frame, text=item.schedule, font=("Arial", 12, "bold"), fg="#34495e", bg="white", justify="left")
        conductor_label.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 0))

        program_label = Label(details_frame, text="$" + str(item.price), font=("Arial", 12), fg="#1a1a1a", bg="white", justify="left")
        program_label.grid(row=2, column=0, sticky="w", padx=5, pady=(10, 0))

        description_frame = Frame(right_frame, bg="white")
        description_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        canvas = Canvas(description_frame, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(description_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        content_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        description_label = Label(content_frame, text=item.detail, font=("Arial", 11), fg="#1a1a1a", bg="white", wraplength=500, justify="left")
        description_label.pack(fill="x", padx=5, pady=(0, 10))

        create_footer( self.root)

    def show_ticket(self, ticket: Ticket):
        self.show_event(ticket)

        text_frame = Frame(self.left_frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        Label(text_frame, text=f"Your Ticket code :  {ticket.ticket_id}", font=("Arial", 14, "bold")).pack()
        Label(text_frame, text=f"You have {ticket.quantity} tickets of this concert", font=("Arial", 14)).pack()

    def show_terms_conditions(self):
        flush(self)
        create_menu(self, self.root)

        main_frame = Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        icon_image = get_image(rf"imgs/Orquesta sinfónica.jpeg", 500, 350)

        image_frame = Label(main_frame, text = " ", font =("Arial", 40), image=icon_image, bg="black")
        image_frame.image = icon_image
        image_frame.pack(fill="x", expand=True, padx=30)

        text = Label(main_frame, text="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut convallis nulla ut ex vehicula, id condimentum augue venenatis. Morbi iaculis nec lectus ac tempor. Nunc ut sapien euismod, viverra justo at, eleifend tortor. Aenean lobortis justo in diam sodales, at fermentum felis mattis. Integer ut tempus augue. Fusce sagittis non tellus a mattis. Aliquam fringilla ipsum neque,\n\n ac pulvinar lacus dapibus eget. Donec vel est id orci lobortis dignissim. Vestibulum pellentesque elit a libero eleifend mollis. In in nibh suscipit, gravida sem et, tincidunt ex. Maecenas lacus massa, ultrices nec rutrum quis, vestibulum in quam. Nam in lectus aliquet, mattis orci ac, egestas massa. Pellentesque a sagittis massa. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.Maecenas sit amet est quis sapien tincidunt volutpat. Etiam consectetur mi eget scelerisque. Morbi facilisis mattis tortor ultrices dignissim. Duis nec convallis augue. Vivamus gravida mollis augue, eu ultricies ante egestas ac.Etiam ac ante augue. Sed eu fringilla augue. Praesent eget pellentesque purus, non """, wraplength=1250, font=("Arial", 12, "bold"), justify="center")
        text.pack(expand=True, fill="both")

        create_footer( self.root)

    def show_about_us(self):
        flush(self)
        create_menu(self, self.root)

        main_frame = Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        icon_image = get_image(rf"imgs/National Symphony Orchestra.jpeg", 500, 350)
        image_frame = Label(main_frame, image=icon_image, bg="black")
        image_frame.image = icon_image
        image_frame.pack(fill="x", expand=True, padx=30)

        text = Label(main_frame, text="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut convallis nulla ut ex vehicula, id condimentum augue venenatis. Morbi iaculis nec lectus ac tempor. Nunc ut sapien euismod, viverra justo at, eleifend tortor. Aenean lobortis justo in diam sodales, at fermentum felis mattis. Integer ut tempus augue. Fusce sagittis non tellus a mattis. Aliquam fringilla ipsum neque,\n\n ac pulvinar lacus dapibus eget. Donec vel est id orci lobortis dignissim. Vestibulum pellentesque elit a libero eleifend mollis. In in nibh suscipit, gravida sem et, tincidunt ex. Maecenas lacus massa, ultrices nec rutrum quis, vestibulum in quam. Nam in lectus aliquet, mattis orci ac, egestas massa. Pellentesque a sagittis massa. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.Maecenas sit amet est quis sapien tincidunt volutpat. Etiam consectetur mi eget scelerisque. Morbi facilisis mattis tortor ultrices dignissim. Duis nec convallis augue. Vivamus gravida mollis augue, eu ultricies ante egestas ac.Etiam ac ante augue. Sed eu fringilla augue. Praesent eget pellentesque purus, non """, wraplength=1250, font=("Arial", 12, "bold"), justify="center")
        text.pack(expand=True, fill="both")

        create_footer( self.root)

    def show_contacts(self):
        flush(self)
        create_menu(self, self.root)

        main_frame = Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        contact1 = Frame(main_frame, height=300, relief="solid", bd=1)
        contact1.pack(fill="x", pady=5, padx=20)

        icon_image = get_image(rf"imgs/conductor1.jpeg", 200, 200)
        image_frame = Label(contact1, image=icon_image, bg="black")
        image_frame.image = icon_image
        image_frame.pack(side="left", padx=5, pady=5)

        text = Label(contact1, text="Sapien tincidunt volutpat. Etiam consectetur mi eget scelerisque. Morbi facilisis mattis tortor ultrices dignissim. Duis nec convallis augue. Vivamus gravida mollis augue, eu ultricies ante egestas ac. Etiam ac ante augue. Sed eu fringilla augue. Praesent eget pellentesque purus, non. \n\nContact : +62 05192813", wraplength=800, font=("Arial", 12, "bold"), justify="left", )
        text.pack(side="left", padx=10)

        contact2 = Frame(main_frame, height=300, relief="solid", bd=1)
        contact2.pack(fill="x", pady=5, padx=20)

        icon_image = get_image(rf"imgs/conductor2.jpeg", 200, 200)
        image_frame = Label(contact2, image=icon_image, bg="black")
        image_frame.image = icon_image
        image_frame.pack(side="right", padx=5, pady=5)

        text = Label(contact2, text="Sapien tincidunt volutpat. Etiam consectetur mi eget scelerisque. Morbi facilisis mattis tortor ultrices dignissim. Duis nec convallis augue. Vivamus gravida mollis augue, eu ultricies ante egestas ac. Etiam ac ante augue. Sed eu fringilla augue. Praesent eget pellentesque purus, non. \n\nContact : +62 05192813", wraplength=800, font=("Arial", 12, "bold"), justify="right", )
        text.pack(side="right", padx=10)

        contact3 = Frame(main_frame, height=300, relief="solid", bd=1)
        contact3.pack(fill="x", pady=5, padx=20)

        icon_image = get_image(rf"imgs/soloist1.jpeg", 200, 200)
        image_frame = Label(contact3, image=icon_image, bg="black")
        image_frame.image = icon_image
        image_frame.pack(side="left", padx=5, pady=5)

        text = Label(contact3, text="Sapien tincidunt volutpat. Etiam consectetur mi eget scelerisque. Morbi facilisis mattis tortor ultrices dignissim. Duis nec convallis augue. Vivamus gravida mollis augue, eu ultricies ante egestas ac. Etiam ac ante augue. Sed eu fringilla augue. Praesent eget pellentesque purus, non. \n\nContact : +62 05192813", wraplength=800, font=("Arial", 12, "bold"), justify="left", )
        text.pack(side="left", padx=10)

        create_footer( self.root)

    def top_up(self):
        
        def add_balance(first_name_entry, last_name_entry, email_entry, balance_entry):
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            balance = balance_entry.get()
            if not first_name or not last_name or not email or not balance:
                messagebox.showwarning("Input Error", "Please fill all fields")
            elif float(balance) < 0:
                messagebox.showwarning("Input Error", "Please fill valid balance")
            else:
                self.sql.update_data("account", self.curr_account.account_id, "wallet", self.curr_account.wallet + float(balance))
                self.curr_account.wallet += float(balance)
                self.wallet_label.config(text=f"Wallet : $ {self.curr_account.wallet:,.2f}")
                messagebox.showinfo("Notice", f"succesfully added {float(balance)} $ to you wallet")
                self.back_to_homepage()
        
        flush(self)
        create_menu(self, self.root)
        create_search_bar(self, "wallet")

        main_frame = Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        canvas = Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = Frame(canvas)
        scrollable_frame.pack(expand=True, fill="both")
        scrollable_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        title_label = Label(scrollable_frame, text="TOP UP YOUR WALLET", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        entries = {}
        first_name = self.curr_account.first_name
        last_name = self.curr_account.last_name
        email = self.curr_account.email

        initial_data = { "First Name": first_name, "Last Name": last_name, "Email": email}

        first_name_label = Label(scrollable_frame, text="First Name", font=("Arial", 12))
        first_name_label.grid(row=1, column=0, sticky='w', pady=5)
        first_name_entry = Entry(scrollable_frame, width=40)
        first_name_entry.insert(0, initial_data["First Name"])
        first_name_entry.grid(row=1, column=1, pady=5)
        entries["First Name"] = first_name_entry

        last_name_label = Label(scrollable_frame, text="Last Name", font=("Arial", 12))
        last_name_label.grid(row=2, column=0, sticky='w', pady=5)
        last_name_entry = Entry(scrollable_frame, width=40)
        last_name_entry.insert(0, initial_data["Last Name"])
        last_name_entry.grid(row=2, column=1, pady=5)
        entries["Last Name"] = last_name_entry

        email_label = Label(scrollable_frame, text="Email", font=("Arial", 12))
        email_label.grid(row=3, column=0, sticky='w', pady=5)
        email_entry = Entry(scrollable_frame, width=40)
        email_entry.insert(0, initial_data["Email"])
        email_entry.grid(row=3, column=1, pady=5)
        entries["Email"] = email_entry

        balance_label = Label(scrollable_frame, text="Balance", font=("Arial", 12))
        balance_label.grid(row=4, column=0, sticky='w', pady=5)
        balance_entry = Entry(scrollable_frame, width=40)
        balance_entry.grid(row=4, column=1, pady=5)

        Label(scrollable_frame, text="Payment Method:", font=("Arial", 12)).grid(row=5, column=0, sticky='w', pady=5)
        payment_method = StringVar()
        payment_method.set("Credit Card") 
        payment_options = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]
        payment_dropdown = OptionMenu(scrollable_frame, payment_method, *payment_options)
        payment_dropdown.grid(row=5, column=1, pady=5)

        send_button = Button(scrollable_frame, text="TOP UP", font=("Arial", 10), command=lambda: add_balance(first_name_entry, last_name_entry, email_entry, balance_entry), bg="#2c3e50", fg="white", width=20)
        send_button.grid(row=6, column=0, columnspan=2, pady=15)

        cancel_label = Label(scrollable_frame, text="CANCEL", font=("Arial", 10), fg="#2c3e50", cursor="hand2")
        cancel_label.grid(row=7, column=0, columnspan=2, pady=15)
        cancel_label.bind("<Button-1>", lambda e: self.back_to_homepage())

    def back_to_homepage(self):
        self.filter_var.set("All Events")
        self.filter_var.set("None")
        self.order.set("Ascending")
        self.homepage()
App()

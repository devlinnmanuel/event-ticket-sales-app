from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from classes import Ticket, Account, Event
from sql import SQL
from sklearn.metrics.pairwise import cosine_similarity

def code_converter(ins, idx):
    return list(ins.events.keys())[idx]

def index_converter(ins, username):
    return list(ins.accounts.keys()).index(username)

def edit_atr(user_attribute, event_attribute, to_edit):
    if to_edit == "add":
        for idx in range(len(event_attribute)):
            user_attribute[idx] += event_attribute[idx]
    elif to_edit == "minus":
        for idx in range(len(event_attribute)):
            user_attribute[idx] -= event_attribute[idx]

def recommend_events(ins, user_preferences, event_attributes, top_n=3):
    user_tickets = list(map(lambda x : x[8], ins.sql.select_ticket(ins.curr_account.account_id)))
    similarity_scores = cosine_similarity(user_preferences, event_attributes).flatten()

    top_indices = similarity_scores.argsort()[-top_n:][::-1] 
    recommendations = [top_indices[i] for i in range(3) if code_converter(ins, top_indices[i]) not in user_tickets]
    
    return recommendations

def get_image(path, width, height):
    pil_image = Image.open(path)
    resized_image = pil_image.resize((width, height), Image.LANCZOS)
    icon_image = ImageTk.PhotoImage(resized_image)
    return icon_image

def filters(data, time_filter = None, search_filter = None, sort_by = "event_name", order = "Ascending"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    filtered_data = data

    if search_filter is not None:
        filtered_data = [item for item in data if search_filter.lower() in item.event_name.lower()]

    if time_filter == "Passed Events":
        filtered_data = [item for item in filtered_data if item.schedule < current_time]
    elif time_filter == "Coming Soon":
        filtered_data = [item for item in filtered_data if item.schedule > current_time]
    elif time_filter == "All Events":
        filtered_data = filtered_data

    rvrs = False if order == "Ascending" else True
    sort_by = "event_name" if sort_by == "Name" else sort_by
    sort_by = sort_by.lower()
    
    filtered_data = sorted(filtered_data, key = lambda x : getattr(x, sort_by), reverse=rvrs)

    return filtered_data

def flush(ins):
    for widget in ins.root.winfo_children():
        widget.destroy()

def create_scrollable_frame(ins):

    
    ins.main_frame = Frame(ins.root)
    ins.main_frame.pack(fill="both", expand=True)
    

    ins.canvas = Canvas(ins.main_frame)
    ins.canvas.pack(side="left", fill="both", expand=True)

    ins.scrollbar = Scrollbar(ins.main_frame, orient="vertical", command=ins.canvas.yview)
    ins.scrollbar.pack(side="right", fill="y")

    ins.scrollable_frame = Frame(ins.canvas)
    ins.scrollable_frame.pack(expand=True, fill="both")
    ins.scrollable_frame.bind("<Configure>", lambda e: ins.canvas.configure(scrollregion=ins.canvas.bbox("all")))
    ins.scrollable_window = ins.canvas.create_window((0, 0), window=ins.scrollable_frame, anchor="nw")

    ins.canvas.configure(yscrollcommand=ins.scrollbar.set)

    ins.canvas.bind("<Configure>", lambda e: ins.canvas.itemconfig(ins.scrollable_window, width=e.width - 5))
    ins.canvas.bind_all("<MouseWheel>", lambda e: ins.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

def create_menu(ins, parent):
    def log_out():
        ins.logged_in = False
        ins.curr_account = None
        ins.homepage()
        messagebox.showinfo("Logout", "You have successfully logged out.")

    ins.menu_frame = Frame(parent, bg="#34495e", height=60)
    ins.menu_frame.pack(side="top", fill="x", padx=0, pady=0)

    home = Label(ins.menu_frame, text="Home", bg="#34495e", fg="white", font=("Arial", 12), cursor="hand2")
    home.bind("<Button-1>", lambda e: ins.homepage())
    home.pack(side="left", padx=10, pady=10)

    about_us = Label(ins.menu_frame, text="About Us", bg="#34495e", fg="white", font=("Arial", 12), cursor="hand2")
    about_us.bind("<Button-1>", lambda e: ins.show_about_us())
    about_us.pack(side="left", padx=10, pady=10)

    terms_and_cons = Label(ins.menu_frame, text="Terms & Conditions", bg="#34495e", fg="white", font=("Arial", 12), cursor="hand2")
    terms_and_cons.bind("<Button-1>", lambda e: ins.show_terms_conditions())
    terms_and_cons.pack(side="left", padx=10, pady=10)

    contacts = Label(ins.menu_frame, text="Contacts", bg="#34495e", fg="white", font=("Arial", 12), cursor="hand2")
    contacts.bind("<Button-1>", lambda e: ins.show_contacts())
    contacts.pack(side="left", padx=10, pady=10)

    if ins.logged_in:

        ins.login_label = Label(ins.menu_frame, bg="#34495e", fg="white", font=("Arial", 12), cursor="hand2")
        ins.login_label.bind("<Button-1>", lambda e: ins.show_cart())

        pil_image = Image.open(rf"imgs/profile.png")
        resized_image = pil_image.resize((30, 30), Image.LANCZOS)
        icon_image = ImageTk.PhotoImage(resized_image)

        ins.login_label.config(image=icon_image)
        ins.login_label.image = icon_image

        my_tickets = [Ticket(ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id,event_name, price, detail, event_photo, schedule, status, genre, quantity) for ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id, event_name, price, detail, event_photo, schedule, status, genre, quantity in ins.sql.select_ticket(ins.curr_account.account_id)]
        menu = Menu(ins.menu_frame, tearoff=0)
        menu.add_command(label="Your Cart", command= lambda : ins.show_cart(my_tickets))
        menu.add_command(label="Your Profile", command=ins.show_profile)
        menu.add_command(label="Logout", command=lambda: log_out())

        ins.login_label.pack(anchor="e", pady=20)
        ins.login_label.bind("<Button-1>", lambda e : menu.post(e.x_root, e.y_root))
        ins.login_label.pack(side="right", padx=10, pady=10)

        ins.wallet_label = Label(ins.menu_frame, text=f"Wallet : $ {ins.curr_account.wallet:,.2f} ", bg="#34495e", fg="white", font=("Arial", 12), cursor="hand2")
        ins.wallet_label.pack(side="right", padx=10, pady=10)
        ins.wallet_label.bind("<Button-1>", lambda e: ins.top_up())
    else:

        ins.login_label = Label(ins.menu_frame, text="Login", bg="#34495e", fg="white", font=("Arial", 12),cursor="hand2")
        ins.login_label.bind("<Button-1>", lambda e: ins.show_login_page())
        ins.login_label.pack(side="right", padx=10, pady=10)

def create_search_bar(ins, mode):
    def on_entry_click(event):
        if search_entry.get() == "Search events":
            search_entry.delete(0, END)
            search_entry.config(fg='black')

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "Search events")
            search_entry.config(fg='grey')

    search_entry = Entry(ins.menu_frame, width=40)
    search_entry.insert(0, "Search events")
    search_entry.bind("<FocusIn>", on_entry_click)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.pack(side="left", padx=10, pady=10)

    pil_sch_image = Image.open(rf"imgs/search.png")
    resized_sch_image = pil_sch_image.resize((15, 15), Image.LANCZOS)
    icon_sch_image = ImageTk.PhotoImage(resized_sch_image)

    ins.search_img = Label(ins.menu_frame, bg="#34495e", fg="white", font=("Arial", 12), cursor="hand2")
    ins.search_img.config(image=icon_sch_image)
    ins.search_img.image = icon_sch_image
    ins.search_img.pack(side="left", padx=10, pady=10)

    if mode == "item":
        ins.search_img.bind("<Button-1>", lambda event: ins.homepage(filters(ins.events.values(), ins.filter_var.get(), search_entry.get(), ins.sort_by_var.get(), ins.order.get()), False))
    elif mode == "tickets":
        my_tickets = [Ticket(ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id,event_name, price, detail, event_photo, schedule, status, genre, quantity) for ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id, event_name, price, detail, event_photo, schedule, status, genre, quantity in ins.sql.select_ticket(ins.curr_account.account_id)]
        ins.search_img.bind("<Button-1>", lambda event: ins.show_cart(filters(my_tickets, ins.filter_var.get(), search_entry.get(), ins.sort_by_var.get(), ins.order.get())))

def create_footer( parent):
    footer = Frame(parent, bg="#2c3e50", height=10)
    footer.pack(side="top", fill="x", padx=0, pady=0)

    Label(footer, text="© 2024 Event Organizer. All rights reserved.", fg="white", bg="#2c3e50",font=("Arial", 12)).pack(side="left", padx=10, pady=5)
    Label(footer, text="Jl. Industri blok B 14 Kav. 1 Kemayoran, Jakarta Pusat 10610 --- +62 8777 100 2009 --- boxoffice@eventorganizer.com", font=("Arial", 12), fg="white", bg="#2c3e50").pack(side="right", pady= 5,padx=10)

def show_items(ins, data: list[Ticket], mode :str, recommendation = False):
    
    def sell_ticket(ins , item : Ticket):
        ins.sql.delete_data("ticket", item.ticket_id)
        ins.curr_account.wallet += float(item.price)
        ins.sql.update_data("account", item.account_id, "wallet", ins.curr_account.wallet)
        ins.show_cart()
        edit_atr(ins.user_preference, ins.events[item.event_name], "minus")
        messagebox.showinfo("Status info", f"Succesfully Sold {item.event_name} for {item.price}")

    for item in data:
        item_frame = Frame(ins.scrollable_frame, bd=1, relief="solid", padx=3, pady=3, cursor="hand2")
        item_frame.pack(fill=X, pady=5, padx=10)

        icon_image = get_image(item.event_photo, 100, 100)
        image_frame = Label(item_frame, image=icon_image, width=100, height=100, bd=2, relief= "raised")
        image_frame.image = icon_image
        image_frame.pack(side="left", fill="y", padx=5, pady=5)

        text_frame = Frame(item_frame, cursor="hand2")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)

        title_frame = Frame(text_frame, cursor="hand2")
        title_frame.pack(fill="x", expand=True, side="top")

        title_label = Label(title_frame, text=item.event_name , font=("Arial", 12, "bold"), anchor="nw", cursor="hand2")
        title_label.pack(side="left")

        genre_label = Label(title_frame, text=f" - {item.genre}" , font=("Arial", 12), anchor="nw", cursor="hand2")
        genre_label.pack(side = "left")

        schedule_label = Label(text_frame, text=item.schedule , font=("Arial", 11), anchor="nw", cursor="hand2")
        schedule_label.pack(side="top", fill="x", expand=True)

        description_label = Label(text_frame, text=item.detail, font=("Arial", 10), anchor="nw", wraplength=1250, justify="left", height=5, cursor="hand2")
        description_label.pack(side="top", fill="x", expand=True)

        if mode == "item":
            func = ins.buy 
            price_label = Label(item_frame,text = f"${item.price}"  , font=("Arial", 12, "bold"))
            price_label.pack(side = "left", fill = "both", padx=5)
        elif mode == "ticket":
            func = ins.show_ticket

            sell_frame = Frame(item_frame)
            sell_frame.pack(side="left", fill="x", padx=10)

            price_label = Label(sell_frame,text = f"${item.price}"  , font=("Arial", 12, "bold"))
            price_label.pack(side="top")
            sell_button = Button(sell_frame, text = "Sell",font=("Arial", 12), bg="red", fg = "white", command = lambda i = item : sell_ticket(ins, i))
            sell_button.pack(side="top")
        
        item_frame.bind("<Button-1>", lambda e, i=item: func(i))
        image_frame.bind("<Button-1>", lambda e, i=item: func(i))
        title_label.bind("<Button-1>", lambda e, i=item: func(i))
        schedule_label.bind("<Button-1>", lambda e, i=item: func(i))
        genre_label.bind("<Button-1>", lambda e, i=item: func(i))
        description_label.bind("<Button-1>", lambda e, i=item: func(i))

    if not recommendation :
        if len(data) == 0:
            Label(ins.scrollable_frame, text="No items available", font=("Arial", 13)).pack()
            Label(ins.scrollable_frame, text=" ", height=40, font=("Arial", 10)).pack()
        elif len(data) == 1:
            Label(ins.scrollable_frame, text=" ", height=30, font=("Arial", 10)).pack()
        elif len(data) == 2:
            Label(ins.scrollable_frame, text=" ", height=21, font=("Arial", 10)).pack()
        elif len(data) == 3:
            Label(ins.scrollable_frame, text=" ", height=15, font=("Arial", 10)).pack()
        elif len(data) == 4:
            Label(ins.scrollable_frame, text=" ", height=4, font=("Arial", 10)).pack()

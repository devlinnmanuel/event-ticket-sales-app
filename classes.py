class Ticket:
    def __init__(self, ticket_id, account_id, first_name, last_name, username, password, email, wallet, event_id,
                 event_name, price, detail, event_photo, schedule, status,genre,  quantity):
        self.ticket_id = ticket_id

        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.wallet = float(wallet)

        self.event_id = event_id
        self.event_name = event_name
        self.price = price
        self.detail = detail
        self.event_photo = event_photo
        self.schedule = schedule
        self.status = status
        self.genre = genre

        self.quantity = quantity

    def __repr__(self):
        return f"{self.ticket_id},{self.account_id},{self.first_name},{self.last_name},{self.username},{self.password},{self.email},{self.wallet},{self.event_id},{self.event_name},{self.price},{self.detail},{self.event_photo},{self.schedule},{self.status},{self.quantity}"


class Event:
    def __init__(self, event_id, event_name, price, detail, event_photo, schedule, status, genre):
        self.event_id = event_id
        self.event_name = event_name
        self.price = price
        self.detail = detail
        self.event_photo = event_photo
        self.schedule = schedule
        self.status = status
        self.genre = genre

    def __repr__(self):
        return f"{self.event_id},{self.event_name},{self.price},{self.detail},{self.event_photo},{self.schedule},{self.status},{self.genre}"


class Account:
    def __init__(self, account_id, first_name, last_name, username, password, email, wallet):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.wallet = wallet

    def __repr__(self):
        return f"{self.account_id},{self.first_name},{self.last_name},{self.username},{self.password},{self.email},{self.wallet}"
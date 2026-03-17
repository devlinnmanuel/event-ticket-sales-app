# Event Ticket Sales Application (Tkinter + MySQL)

A desktop-based **Event Ticket Sales Application** developed using Python (Tkinter) for the graphical user interface and MySQL as the database system.
This application allows users to browse events, purchase tickets, manage their accounts, and receive simple AI-based event recommendations. This project was developed as part of the Database Systems project.

## Features

### User Management

- User registration.
- User login.
- Profile management.
- Wallet top-up system.

### Ticket System

- Browse available events.
- View event details.
- Purchase event tickets.
- View purchased tickets in cart.
- Refund / delete tickets (optional).

### Database Integration

- MySQL database integration using ```bash mysql.connector```
- Full CRUD operations (Create, Read, Update, Delete).

### Simple AI Recommendation

- AI-based recommendation system that suggests events to users based on their preferences.
- The recommendation system uses **Cosine Similarity** and ```bash sklearn.metrics.pairwise```
- Analyzes the genres of events that a user has previously purchased and recommends similar events.

### Database Transactions

- MySQL transaction mechanisms are implemented to maintain data integrity during Update and Delete operations.

## CRUD Implementation

- **Create**: Create user accounts and purchase tickets.
- **Read**: Display events and user tickets.
- **Update**: Update user profile information.
- **Delete**: Refund tickets and remove them from database.

## Technologies Used

- Python
- Tkinter (GUI Framework)
- MySQL
- mysql-connector-python
- Scikit-learn

## Database Structure

The database used in this project is called:
```bash
event_db
```
Main entities in the system:
- Account
- Event
- Ticket
- Event Attribute

Relationships:
- A user can purchase multiple tickets
- An event can have multiple participants
- Event attributes define the category or genre of an event

## Application Interface

The application provides several GUI pages, all of which are built using Tkinter GUI components:
- Homepage
- Login Page
- Create Account
- Profile Page
- Event Details
- Cart / Purchased Tickets
- Wallet Top-up
- Terms & Conditions
- About Us
- Contact Page

## Installation

**1. Clone the Repository**
```bash
git clone https://github.com/devlinmanuel/event-ticket-sales-app.git
cd event-ticket-sales-app
```
**2. Install Required Dependencies** (python libraries)
```bash 
pip install mysql-connector-python scikit-learn
```
**3. Setup MySQL Database**

Make sure MySQL installed and running. The application will automatically attempt to create the required database and tables when it first connects. Then, adjust the MySQL credentials in the the python code (```sql.py```):
```bash 
mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD"
)
```

## Running the App

Make sure the application file you want to run is located in the project directory. Then, run the app from the terminal (this will start the Tkinter GUI application): 
```bash 
python app.py
```

## AI Recommendation Logic

1. Collecting user ticket history
2. Extracting event attributes (genres / categories)
3. Creating preference vectors
4. Calculating cosine similarity between **user preferences** and **available events**
5. Suggesting the most similar events to users

# PythonForDataScience
## FINTRAKK - Personel Expenses Trancking System
Fintrakk is a Python-based **Personal Finance and Expense Tracking System** that allows users to monitor and manage their financial activities. It provides **data storage, statistical analysis, and visualizations** to help users understand their income and expenses efficiently.

---
## Description

## Functionalities
### 1. Data source and retrieval
- Users can **input financial transactions** manually.
- Supports **real-time exchange rate retrieval** for multi-currency transactions.
- Data fetched and stored securely in **SQLite/PostgreSQL database**.

### 2. Data storage and handling
- Transactions stored with fields: **Date, Category, Type, Amount, Account**.
- Supports **user authentication** (registration, login, logout).
- Uses **hashed passwords for security**.
- Django ORM used for managing the database.

### 3. Interface
- Built with **Django framework** for a clean and responsive UI.
- Bootstrap-based **navigation & dashboard** for better user experience.
- **Sidebar navigation** for quick access to different functionalities.

### 4. Statistical analysis
- Provides **total balance** and **total number of transactions**.
- Tracks **category-wise spending patterns**.
- Identifies **income vs. expense trends** over time.
- Supports **multiple accounts & categories**.

### 5. Visualizations
- Users can view expenses using:
  - **Bar charts**
  - **Pie charts**
  - **Line graphs**
- Interactive **Get Report** section for filtering transactions.
- Option to **download charts as PNG files**.

---

## Installation and Usage
### **1. Clone the Repository**
- git clone https://github.com/Krishnachowdary711/Spartans.git
- cd fintrakk-expense-tracker
### **2. Create and Activate Virtual Environment**
- python -m venv venv
- source venv/bin/activate  # For Mac/Linux
- venv\Scripts\activate  # For Windows
### **3. Install Dependencies**
- pip install -r requirements.txt
### **4. Apply Migrations**
- python manage.py migrate
### **5. Create Superuser (Optional)**
- python manage.py createsuperuser
### **6. Run the Server**
- python manage.py runserver

- Open your Browser and access the app at http://127.0.0.1:8000/

## Tools & libraries
	•	Python 3.x (Core programming language)
	•	Django (Web framework)
	•	SQLite/PostgreSQL (Database)
	•	Matplotlib & Pandas (Data analysis & visualization)
	•	Bootstrap 5 (Front-end UI styling)
	•	FontAwesome (Icons)
	•	Requests (For fetching exchange rates)

## Timeline

## Group Details
* Group name:
* Group code: 
* Group repository:
* Tutor responsible:
* Group team leader:
* Group members: 


## Future improvements

## Acknowledgement

# PythonForDataScience
![image](https://github.com/user-attachments/assets/d9459c3a-414b-41de-9509-316f96b78824)

## FINTRAKK - Personal Expenses Tracking System



## Description
* Fintrakk is a Python-based tool that helps users track and manage their finances by providing data storage, statistical analysis, and visualizations. The goal is to simplify financial management and offer insights into spending patterns. This project was chosen to help individuals gain better control over their finances through an intuitive and data-driven approach. To achieve this, Fintrakk integrates secure data storage, expense categorization, budgeting, statistical analysis, and interactive visualizations. These features allow users to monitor income, set budgets, analyze trends, and make informed financial decisions effortlessly.
---

## Functionalities
### 1. Data source and retrieval
- Users can **input financial transactions** manually.
- Supports **real-time exchange rate retrieval** for multi-currency transactions.
- Data fetched and stored securely in **SQLite database**.

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
- cd Spartans/fintrakk
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
- Python 3.x (Core programming language)
- Django (Web framework)
- SQLite (Database)
- Matplotlib & Pandas (Data analysis & visualization)
- Bootstrap 5 (Front-end UI styling)
- FontAwesome (Icons)
- Requests (For fetching exchange rates)

## Timeline
![image](https://github.com/user-attachments/assets/ab949004-ff39-4e6a-bb42-57d806b3b7fb)

## Group Details
* Group name: Spartans
* Group code: G06
* Group repository: Spartans
* Tutor responsible: David Wode
* Group team leader: Krishna Sai
* Group members: Ruthran Veerasamy Balakrishnan, Krishna Sai
* Krishna contributed to the design and development of the UI/UX for the webpage, along with implementing the transactions and currency conversion columns. Meanwhile, Ruthran worked on the Accounts and Categories columns. Finally, both collaborated to develop the report generation column.
## Future improvements
- Increase More features in the existing model like, Integrating it with banking app.
- Budget planning & alerts for overspending.
- Interactive Visualization Techniques

## Acknowledgement
We sincerely appreciate the valuable contributions and support from the following individuals, as well as Georg August University, throughout the development of this project.

* Prof. Bela Gipp & Gipp Lab: We are deeply thankful for the opportunity to participate in the lecture and group project under your guidance and mentorship.
* David Wode: Our tutor, whose insightful feedback and guidance were helpful in shaping our project and enhancing our understanding.
* Terry Lima Ruas: Our lecturer whose expertise and encouragement significantly contributed to the success and growth of our project.

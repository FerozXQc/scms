**Stadium Complex Management System**

A simple web application built with Flask and MySQL for managing a stadium complex. The system currently supports basic CRUD operations for handling stadium-related data.

_Note: The update and delete features are not yet implemented, and there is no admin dashboard at this time._


**Features**

    Add and view stadium information

    Manage events and bookings

    (Missing) Update and delete operations

    (Missing) Admin dashboard


**Technologies Used**

    Flask - Web framework for Python

    MySQL - Database management system

    flask_mysqldb - Flask extension for MySQL integration

    python-decouple - For separating configuration from code

    requests - For making HTTP requests


**Setup Instructions**

Clone the repository:

    git clone https://github.com/yourusername/stadium-complex-management.git

Install dependencies:

pip install -r requirements.txt

Set up the Database:

    Download the provided .db file and place it in the root directory of the project. This file contains the pre-configured database.

Configure Environment Variables:

    Create a .env file in the root directory and add the following variables:

    MYSQL_USER=your_mysql_username
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_HOST=localhost
    MYSQL_DB=your_database_name

    Replace your_mysql_username, your_mysql_password, and your_database_name with the appropriate values for your MySQL setup.

Run the app:

python app.py

Access the application: Open your browser and go to http://localhost:5000 to access the app.


**Additional Notes:**

    This project was created as part of my school project. 

    Make sure your MySQL server is running locally (or use your own MySQL database setup).

    The .env file will be automatically loaded by the python-decouple package, which allows you to separate your sensitive credentials from your code.

**License**

MIT License

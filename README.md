# college canteen
🍔 College Canteen Management System
A full-stack web application built using Python Flask that automates canteen operations. This system allows students to order food online using a digital wallet, while administrators manage the menu, users, orders, and transactions.

🚀 Features
👨‍💻 Admin Panel
User Management: Register, view, update, and delete student accounts.

Menu Management: Add, edit, and delete food items (including photo uploads).

Order Management: View incoming orders in real-time with options to Accept or Reject.

Wallet System: Add funds (points/money) to specific student accounts.

Transaction History: View logs of wallet recharges.

Profile Management: Update admin details and profile picture.

🎓 Student Panel
Digital Menu: Browse food items with prices and availability.

Cart System: Add items to cart, update quantities, and view cart summary.

Wallet Payment: Pay for orders directly using the student wallet balance.

Order History: View status of past orders (Pending, Accepted, Rejected).

Profile: View personal details and wallet balance.

🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML, CSS, JavaScript (AJAX for cart operations)

Database: MySQL (via mysql-connector or similar in MyLib)

File Handling: Werkzeug secure_filename for image uploads

📂 Project Structure
Plaintext

/Project_Root
│
├── app.py                # Main application entry point
├── MyLib.py              # Database connection and helper functions
├── /static
│   ├── /photos           # User profile pictures
│   ├── /item_photos      # Food menu images
│   ├── /css              # Stylesheets
│   └── /js               # Scripts
│
├── /templates            # HTML files (jinja2)
│   ├── home.html
│   ├── admin_profile.html
│   ├── user_home.html
│   ├── order.html
│   └── ... (other templates)
│
└── README.md
⚙️ Installation & Setup
1. Prerequisites
Ensure you have Python installed. You will need to install Flask and the database connector used in your MyLib.py.

Bash

pip install flask
# If using mysql-connector
pip install mysql-connector-python
2. Database Setup
You need to create a database with the following tables (inferred from the code). Run these SQL commands in your database:

SQL

-- Login Credentials Table
CREATE TABLE login_data (
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(100),
    usertype VARCHAR(20)
);

-- Admin Details
CREATE TABLE admin_data (
    name VARCHAR(100),
    address VARCHAR(255),
    contact VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (email) REFERENCES login_data(email)
);

-- Student/User Details
CREATE TABLE user_data (
    st_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10),
    address VARCHAR(255),
    contact VARCHAR(20),
    email VARCHAR(100),
    balance INT DEFAULT 0
);

-- Food Menu
CREATE TABLE food_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price INT,
    type VARCHAR(50),
    photo VARCHAR(255),
    availability VARCHAR(20) DEFAULT 'yes'
);

-- Cart (Temporary Storage)
CREATE TABLE cart_items (
    user_email VARCHAR(100),
    item_id INT,
    quantity INT,
    PRIMARY KEY (user_email, item_id)
);

-- Orders
CREATE TABLE order_data (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(100),
    quantity INT,
    total_price INT,
    type VARCHAR(50),
    st_id INT,
    status VARCHAR(20) DEFAULT 'pending',
    order_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profile Photos
CREATE TABLE photo_data (
    email VARCHAR(100),
    photo VARCHAR(255)
);

-- Wallet Transactions
CREATE TABLE transactions_history (
    pt_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    email VARCHAR(100),
    amount INT,
    st_id INT
);
3. File System Setup
Ensure the following directories exist to store uploaded images:

./static/photos

./static/item_photos

4. Running the Application
Run the application using the command:

Bash

python app.py
Access the app in your browser at: http://127.0.0.1:5000/

🔑 Key Functionalities Explained
Authentication
The app uses session management to handle logins.

Admin Login: Redirects to Order Management Dashboard.

User Login: Redirects to the Food Menu.

Shopping Cart Logic
The cart uses AJAX (/update_cart, /delete_cart) to update quantities dynamically without reloading the page. The data is stored in the cart_items SQL table to persist the cart even if the user logs out.

Order Processing
Student places an order -> Balance is checked against user_data.

Order is saved to order_data with status pending.

Admin sees the order in /show_orders.

Admin clicks Accept/Reject -> Status updates in DB.

🛡️ Security Notes
Secret Key: The app uses a session secret key (app.secret_key). In a production environment, change this to a random environment variable.

File Uploads: Uses werkzeug.utils.secure_filename to prevent malicious file naming attacks.

🤝 Contribution
Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes.

Push to the branch.

Open a Pull Request.
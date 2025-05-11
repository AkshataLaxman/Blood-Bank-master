# Blood Bank Management System

A comprehensive web application built with Flask to manage blood donations, user profiles, and donation requests for blood banks.

## ✨ Features

- **User Authentication System**
  - Secure login and registration with password hashing
  - User profile management
  - Admin and regular user roles

- **Blood Inventory Management**
  - Add, edit, and delete blood donations
  - Track blood quantity by blood type
  - Manage donor information

- **Blood Request System**
  - Request blood from registered donors
  - In-app notification system for blood requests
  - Contact management between donors and recipients

- **Dashboard & Analytics**
  - Visual representation of available blood inventory
  - Total blood units available by blood type
  - User statistics and donation history

- **Search Functionality**
  - Find donors by blood type
  - Search donors by name

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Security**: Werkzeug Security for password hashing
- **Frontend**: HTML, CSS, JavaScript (templates not included in this repository)

## 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AkshataLaxman/blood-bank-management.git
   cd blood-bank-management
   ```

2. **Create and activate a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required packages**
   ```bash
   pip install flask werkzeug
   ```

4. **Initialize the database**
   - The database will be automatically initialized when you run the application for the first time

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your web browser and navigate to `http://localhost:5000`

## 💾 Database Structure

The application uses SQLite with three main tables:

### 1. Users Table
```
- name: User's full name
- addr: User's address
- city: User's city
- pin: Postal/ZIP code
- bg: Blood group
- email: User's email (unique)
- pass: Hashed password
```

### 2. Blood Table
```
- id: Auto-incremented unique ID
- type: Blood type (A+, B-, etc.)
- donorname: Name of the donor
- donorsex: Gender of the donor
- qty: Quantity of blood donated (units)
- dweight: Donor's weight
- donoremail: Donor's email
- phone: Donor's phone number
```

### 3. Request Table
```
- id: Auto-incremented unique ID
- toemail: Recipient's email
- formemail: Requester's email
- toname: Recipient's name
- toaddr: Recipient's address
```

## 👥 User Roles

### Regular Users
- Register and maintain their profile
- Search for donors by blood type or name
- Request blood from registered donors
- Receive and manage notifications for blood requests
- View available blood inventory

### Admin User
- Access all regular user features
- Manage all blood inventory entries (add, edit, delete)
- Delete user accounts
- View comprehensive dashboard with statistics
- Login credentials: 
  - Email: admin@bloodbank.com
  - Password: admin

## 📚 Usage Guide

### For Regular Users

1. **Registration**
   - Navigate to the registration page `/reg`
   - Fill in your personal details and submit

2. **Login**
   - Navigate to the login page `/login`
   - Enter your email and password

3. **Profile Management**
   - View and edit your profile at `/myprofile/<your-email>`

4. **Search for Donors**
   - Use the search function on the index page
   - Select search type (blood type or donor name)
   - Enter search value and submit

5. **Request Blood**
   - Find a donor with compatible blood type
   - Click on "Contact for Blood" next to their profile
   - Fill in required details and submit your request

6. **View Notifications**
   - Check your notifications at `/notifications`
   - Respond to or delete blood requests

### For Administrators

1. **Login as Admin**
   - Use admin credentials to access admin features
   - Email: admin@bloodbank.com
   - Password: admin

2. **Dashboard Access**
   - Navigate to `/dashboard` to view blood inventory statistics

3. **Manage Blood Inventory**
   - Add new blood entries at `/bloodbank`
   - Edit entries via `/editdonor/<id>`
   - Delete entries using the delete function

4. **User Management**
   - View all registered users
   - Delete users if necessary


## 🔒 Security Considerations

- Passwords are securely hashed using Werkzeug Security's generate_password_hash
- Session management with Flask sessions
- Role-based access control for admin functions
- Input validation and error handling

## 🌟 Contributing

Contributions to improve the Blood Bank Management System are welcome:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a Pull Request

## 📄 License

This project is licensed under the Self License.

---

Developed with ❤️ for blood banks and donors everywhere.

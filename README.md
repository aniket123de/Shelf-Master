# Shelf Master

## Overview
The Library Management System is a Python-based application designed to manage books and users in a library. It supports adding books, registering users, issuing and returning books, and searching for books. It also provides a GUI (Graphical User Interface) for ease of use and stores data in a centralized MySQL database.

---

## Features
- Add new books and users.
- Issue books to registered users.
- Return books to the library.
- Search for books by title, author, or ISBN.
- List all available books and registered users.
- GUI interface built using `tkinter`.
- Centralized database to synchronize data across multiple users.

---

## Requirements

### 1. Software
- Python 3.8+
- MySQL Server (local or remote)
- MySQL Workbench (optional, for database management)
- NSIS (optional, for creating an installer)

### 2. Python Libraries
Install the required Python libraries by running:
```bash
pip install mysql-connector-python
```

---

## Setup Instructions

### 1. Clone the Repository
Download or clone the project to your local machine:
```bash
git clone <repository_link>
cd library-management
```

### 2. Database Configuration

#### (a) Create the Database and Tables
1. Open MySQL Workbench or any SQL client.
2. Run the following SQL commands to create the database and tables:
   ```sql
   CREATE DATABASE library_management;
   USE library_management;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL
   );

   CREATE TABLE books (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       author VARCHAR(255),
       isbn VARCHAR(20),
       quantity INT NOT NULL
   );

   CREATE TABLE transactions (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT NOT NULL,
       book_id INT NOT NULL,
       action ENUM('issue', 'return') NOT NULL,
       date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users(id),
       FOREIGN KEY (book_id) REFERENCES books(id)
   );
   ```

#### (b) Enable Remote Access (Optional)
For a centralized database, configure MySQL to allow remote access:
1. Update the MySQL configuration file (`my.cnf` or `my.ini`):
   ```ini
   [mysqld]
   bind-address = 0.0.0.0
   ```
2. Restart the MySQL service.
3. Grant permissions:
   ```sql
   GRANT ALL PRIVILEGES ON library_management.* TO 'root'@'%' IDENTIFIED BY 'your_password';
   FLUSH PRIVILEGES;
   ```

### 3. Update Database Credentials
Modify the `Library` class in `library.py` to include your MySQL credentials:
```python
self.conn = mysql.connector.connect(
    host="your_server_ip_or_domain",  # Use 'localhost' for local databases
    user="your_username",
    password="your_password",
    database="library_management"
)
```

### 4. Run the Application
1. Open a terminal in the project directory.
2. Run the Python script:
   ```bash
   python library.py
   ```

---

## GUI Interface
The application includes a GUI built using `tkinter`. The GUI supports the following actions:
- Adding books and users.
- Issuing and returning books.
- Searching and listing books.

To run the GUI version, execute the same `library.py` file.

---

## Packaging into an Executable

### Step 1: Generate Executable File
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the following command to create the `.exe` file:
   ```bash
   pyinstaller --onefile --windowed --icon=path/to/icon.ico library.py
   ```
3. The executable will be available in the `dist` folder.

### Step 2: Create an Installer
1. Install NSIS from [nsis.sourceforge.io](https://nsis.sourceforge.io/Download).
2. Create a `.nsi` script for the installer, and compile it using NSIS.

---

## Troubleshooting
- **Error: No connection to the database:**
  Ensure the database credentials are correct and the MySQL server is running.

- **Table does not exist:**
  Verify that the `library_management` database and required tables are created.

- **Remote connection issues:**
  Check the MySQL server’s remote access settings.

---

## Future Improvements
- Add user authentication.
- Implement reporting features (e.g., issued books report).
- Enhance the GUI with advanced features (e.g., dropdown menus, filters).
- Migrate to a web-based interface for broader accessibility.

---

## License
This project is open-source and distributed under the MIT License.

---

## Author
Aniket De  
Feel free to contribute and provide feedback!


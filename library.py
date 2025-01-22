import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class Library:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="6289173377@A",  # Replace with your MySQL password
                database="library_management"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print("Error connecting to MySQL database:", e)

    def add_book(self, title, author, isbn, quantity):
        try:
            self.cursor.execute(
                "INSERT INTO books (title, author, isbn, quantity) VALUES (%s, %s, %s, %s)",
                (title, author, isbn, quantity)
            )
            self.conn.commit()
            return f"Book '{title}' added successfully!"
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def add_user(self, name, user_id=None):
        try:
            if user_id:
                # Add user with a specific user_id
                self.cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, name))
            else:
                # Auto-increment user_id
                self.cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            self.conn.commit()
            return f"User '{name}' added successfully!"
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def delete_user(self, user_id):
        try:
            # Check if the user exists
            self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = self.cursor.fetchone()
            
            if not user:
                return f"User with ID {user_id} does not exist."

            # Delete the user
            self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.conn.commit()
            return f"User with ID {user_id} deleted successfully!"
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def issue_book(self, user_id, book_id):
        try:
            # Check if user exists
            self.cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            if not self.cursor.fetchone():
                return "Error: User not found."

            # Check if the book is available
            self.cursor.execute("SELECT quantity FROM books WHERE id = %s", (book_id,))
            result = self.cursor.fetchone()
            if result and result[0] > 0:
                # Update book quantity and log transaction
                self.cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = %s", (book_id,))
                self.cursor.execute(
                    "INSERT INTO transactions (user_id, book_id, action) VALUES (%s, %s, 'issue')",
                    (user_id, book_id)
                )
                self.conn.commit()
                return "Book issued successfully!"
            else:
                return "Error: Book not available."
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def return_book(self, user_id, book_id):
        try:
            # Check if user exists
            self.cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            if not self.cursor.fetchone():
                return "Error: User not found."

            # Check if the user has borrowed the book
            self.cursor.execute(
                "SELECT id FROM transactions WHERE user_id = %s AND book_id = %s AND action = 'issue'",
                (user_id, book_id)
            )
            result = self.cursor.fetchone()
            if result:
                # Update book quantity and log transaction
                self.cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id = %s", (book_id,))
                self.cursor.execute(
                    "INSERT INTO transactions (user_id, book_id, action) VALUES (%s, %s, 'return')",
                    (user_id, book_id)
                )
                self.conn.commit()
                return "Book returned successfully!"
            else:
                return "Error: No record of this book being issued to the user."
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def search_books(self, query):
        try:
            self.cursor.execute(
                "SELECT id, title, author, isbn, quantity FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s",
                (f"%{query}%", f"%{query}%", f"%{query}%")
            )
            results = self.cursor.fetchall()
            if results:
                result_str = "Search Results:\n"
                for book in results:
                    result_str += f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Quantity: {book[4]}\n"
                return result_str
            else:
                return "No books found."
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def list_books(self):
        try:
            self.cursor.execute("SELECT id, title, author, isbn, quantity FROM books")
            results = self.cursor.fetchall()
            if results:
                result_str = "Books in the Library:\n"
                for book in results:
                    result_str += f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Quantity: {book[4]}\n"
                return result_str
            else:
                return "No books in the library."
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def list_users(self):
        try:
            self.cursor.execute("SELECT id, name FROM users")
            results = self.cursor.fetchall()
            if results:
                result_str = "Registered Users:\n"
                for user in results:
                    result_str += f"ID: {user[0]}, Name: {user[1]}\n"
                return result_str
            else:
                return "No users registered."
        except mysql.connector.Error as e:
            return f"Error: {e}"

    def close(self):
        self.conn.close()


class LibraryGUI:
    def __init__(self, root):
        self.library = Library()

        # Root Window Configuration
        self.root = root
        self.root.title("Shelf Master by Aniket")
        self.root.geometry("600x400")  # Set a fixed window size
        self.root.resizable(False, False)  # Disable resizing

        # Header Section
        self.header_frame = tk.Frame(root, bg="#4CAF50", pady=10)
        self.header_frame.pack(fill="x")

        self.label = tk.Label(
            self.header_frame,
            text="Shelf Master by Aniket",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#4CAF50"
        )
        self.label.pack()

        # Main Section
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Group Buttons into Frames
        self.book_frame = tk.LabelFrame(self.main_frame, text="Books", font=("Helvetica", 12, "bold"), padx=10, pady=10)
        self.book_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.user_frame = tk.LabelFrame(self.main_frame, text="Users", font=("Helvetica", 12, "bold"), padx=10, pady=10)
        self.user_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.action_frame = tk.LabelFrame(self.main_frame, text="Actions", font=("Helvetica", 12, "bold"), padx=10, pady=10)
        self.action_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Book Operations
        ttk.Button(self.book_frame, text="Add Book", command=self.add_book).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(self.book_frame, text="Search Books", command=self.search_books).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(self.book_frame, text="List Books", command=self.list_books).grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # User Operations
        ttk.Button(self.user_frame, text="Add User", command=self.add_user).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(self.user_frame, text="Delete User", command=self.delete_user).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(self.user_frame, text="List Users", command=self.list_users).grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Actions (Issue/Return Books)
        ttk.Button(self.action_frame, text="Issue Book", command=self.issue_book).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(self.action_frame, text="Return Book", command=self.return_book).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Adjust grid weight for proper scaling
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    # Methods for Library Operations
    def add_book(self):
        try:
            title = self.ask_input("Enter book title:")
            author = self.ask_input("Enter book author:")
            isbn = self.ask_input("Enter book ISBN:")
            quantity = int(self.ask_input("Enter quantity:"))
            result = self.library.add_book(title, author, isbn, quantity)
            messagebox.showinfo("Result", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")

    def add_user(self):
        try:
            name = self.ask_input("Enter user name:")
            user_id = self.ask_input("Enter user ID (optional):")
            if user_id:  # If user_id is provided
                result = self.library.add_user(name, int(user_id))
            else:  # Auto-increment user_id
                result = self.library.add_user(name)
            messagebox.showinfo("Result", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")

    def delete_user(self):
        try:
            user_id = int(self.ask_input("Enter user ID to delete:"))
            result = self.library.delete_user(user_id)
            messagebox.showinfo("Result", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    def issue_book(self):
        try:
            user_id = int(self.ask_input("Enter user ID:"))
            book_id = int(self.ask_input("Enter book ID:"))
            result = self.library.issue_book(user_id, book_id)
            messagebox.showinfo("Result", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {e}")

    def return_book(self):
        try:
            user_id = int(self.ask_input("Enter user ID:"))
            book_id = int(self.ask_input("Enter book ID:"))
            result = self.library.return_book(user_id, book_id)
            messagebox.showinfo("Result", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {e}")

    def search_books(self):
        try:
            query = self.ask_input("Enter search query (title/author/ISBN):")
            result = self.library.search_books(query)
            messagebox.showinfo("Search Results", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search books: {e}")

    def list_books(self):
        try:
            result = self.library.list_books()
            messagebox.showinfo("Books in Library", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list books: {e}")

    def list_users(self):
        try:
            result = self.library.list_users()
            messagebox.showinfo("Registered Users", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list users: {e}")

    def ask_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def close(self):
        self.library.close()



if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()

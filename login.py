import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Function to register a new user
def register_user():
    username = entry_reg_username.get()
    password = entry_reg_password.get()
    
    if username == "" or password == "":
        messagebox.showwarning("Input Error", "Both fields are required!")
        return
    
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        entry_reg_username.delete(0, tk.END)
        entry_reg_password.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# Function to login
def login_user():
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    
    if result:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Create the main window
root = tk.Tk()
root.title("Call a Doctor")

# Create a frame for the login
frame_login = tk.Frame(root)
frame_login.pack(pady=10)

tk.Label(frame_login, text="Login", font=("Arial", 16)).pack()
tk.Label(frame_login, text="Username").pack()
entry_login_username = tk.Entry(frame_login)
entry_login_username.pack()

tk.Label(frame_login, text="Password").pack()
entry_login_password = tk.Entry(frame_login, show="*")
entry_login_password.pack()

tk.Button(frame_login, text="Login", command=login_user).pack(pady=5)

# Create a frame for the registration
frame_register = tk.Frame(root)
frame_register.pack(pady=10)

tk.Label(frame_register, text="Register", font=("Arial", 16)).pack()
tk.Label(frame_register, text="Username").pack()
entry_reg_username = tk.Entry(frame_register)
entry_reg_username.pack()

tk.Label(frame_register, text="Password").pack()
entry_reg_password = tk.Entry(frame_register, show="*")
entry_reg_password.pack()

tk.Button(frame_register, text="Register", command=register_user).pack(pady=5)

root.mainloop()

# Close the database connection
conn.close()

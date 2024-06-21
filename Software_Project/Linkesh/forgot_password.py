import customtkinter as ctk  # Importing the custom tkinter library as ctk
from tkinter import messagebox  # Importing the messagebox module from tkinter for displaying messages
import mysql.connector  # Importing the MySQL Connector Python module
from mysql.connector import Error  # Importing the Error class from mysql.connector

# Function to go back to the main login page
def back_to_login(window):
    window.destroy()  # Destroying the current window
    import main_page  # Importing the main_page module
    main_page.create_login_window()  # Calling the create_login_window function from main_page

# Function to reset the password
def reset_password():
    username = username_entry.get()  # Getting the username from the username_entry widget
    new_password = new_password_entry.get()  # Getting the new password from the new_password_entry widget
    confirm_password = confirm_password_entry.get()  # Getting the confirm password from the confirm_password_entry widget
    
    # Checking if any of the fields are empty
    if username == "" or new_password == "" or confirm_password == "":
        messagebox.showerror("Error", "Please fill out all fields")  # Displaying an error message if any field is empty
        return
    
    # Checking if the new password matches the confirm password
    if new_password == confirm_password:
        try:
            # Establishing a connection to MySQL database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='calladoctor1234',
                database='calladoctor'
            )
            cursor = connection.cursor()  # Creating a cursor object
            cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))  # Executing a SELECT query
            result = cursor.fetchone()  # Fetching the result of the query
            
            # If username exists in the database
            if result:
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))  # Updating password
                connection.commit()  # Committing the transaction
                connection.close()  # Closing the database connection
                messagebox.showinfo("Success", "Password reset successfully")  # Showing success message
                forgot_password_window.destroy()  # Destroying the current window
                import main_page  # Importing the main_page module
                main_page.create_login_window()  # Calling the create_login_window function from main_page
            else:
                connection.close()  # Closing the database connection
                messagebox.showerror("Error", "Username not found")  # Showing error message if username is not found
        except Error as e:
            print(f"The error '{e}' occurred")  # Printing the error message
            messagebox.showerror("Error", f"An error occurred: {e}")  # Showing error message in messagebox
    else:
        messagebox.showerror("Error", "Passwords do not match")  # Showing error message if passwords don't match

# Create forgot password window
def create_forgot_password_window():
    global forgot_password_window, username_entry, new_password_entry, confirm_password_entry  # Declaring global variables
    
    ctk.set_appearance_mode("light")  # Setting appearance mode to light
    ctk.set_default_color_theme("blue")  # Setting default color theme to blue
    
    forgot_password_window = ctk.CTk()  # Creating a custom tkinter window
    forgot_password_window.title("Forgot Password")  # Setting window title
    forgot_password_window.geometry("400x430")  # Setting window geometry
    
    # Creating labels and entries for username, new password, and confirm password
    username_label = ctk.CTkLabel(forgot_password_window, text="Username")
    username_label.pack(pady=10)
    username_entry = ctk.CTkEntry(forgot_password_window)
    username_entry.pack(pady=10)
    
    new_password_label = ctk.CTkLabel(forgot_password_window, text="New Password")
    new_password_label.pack(pady=10)
    new_password_entry = ctk.CTkEntry(forgot_password_window, show='*')
    new_password_entry.pack(pady=10)
    
    confirm_password_label = ctk.CTkLabel(forgot_password_window, text="Confirm Password")
    confirm_password_label.pack(pady=10)
    confirm_password_entry = ctk.CTkEntry(forgot_password_window, show='*')
    confirm_password_entry.pack(pady=10)
    
    # Button to reset password and back button to return to login page
    reset_password_button = ctk.CTkButton(forgot_password_window, text="Reset Password", command=reset_password)
    reset_password_button.pack(pady=20)
    
    back_button = ctk.CTkButton(forgot_password_window, text="Back", command=lambda: back_to_login(forgot_password_window))
    back_button.pack(pady=10)
    
    forgot_password_window.mainloop()  # Running the main loop for the window

if __name__ == "__main__":
    create_forgot_password_window()  # Calling the create_forgot_password_window function if the script is executed directly

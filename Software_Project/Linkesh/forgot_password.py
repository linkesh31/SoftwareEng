import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Function to go back to the main login page
def back_to_login(window):
    window.destroy()
    import main_page
    main_page.create_login_window()

# Function to reset the password
def reset_password():
    username = username_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()
    if username == "" or new_password == "" or confirm_password == "":
        messagebox.showerror("Error", "Please fill out all fields")
        return
    if new_password == confirm_password:
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='calladoctor1234',
                database='calladoctor'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Password reset successfully")
                forgot_password_window.destroy()
                import main_page
                main_page.create_login_window()
            else:
                connection.close()
                messagebox.showerror("Error", "Username not found")
        except Error as e:
            print(f"The error '{e}' occurred")
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Passwords do not match")

# Create forgot password window
def create_forgot_password_window():
    global forgot_password_window, username_entry, new_password_entry, confirm_password_entry
    ctk.set_appearance_mode("light")  # Modes: "light", "dark", "system"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    forgot_password_window = ctk.CTk()
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("400x430")

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

    reset_password_button = ctk.CTkButton(forgot_password_window, text="Reset Password", command=reset_password)
    reset_password_button.pack(pady=20)

    back_button = ctk.CTkButton(forgot_password_window, text="Back", command=lambda: back_to_login(forgot_password_window))
    back_button.pack(pady=10)

    forgot_password_window.mainloop()

if __name__ == "__main__":
    create_forgot_password_window()

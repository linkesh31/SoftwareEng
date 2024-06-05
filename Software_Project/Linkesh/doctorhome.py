import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os

# Function for button actions
def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def list_of_patients_action():
    messagebox.showinfo("List of Patients", "List of Patients Button Clicked")

def profile_action():
    messagebox.showinfo("Profile", "Profile Button Clicked")

def availability_status_action():
    messagebox.showinfo("Availability Status", "Availability Status Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

# Function to create a connection to the MySQL database
def create_connection(host='localhost', username='root', password='calladoctor1234', database='calladoctor'):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=database
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Function to fetch doctor's full name based on username
def fetch_doctor_fullname(connection, username,fullname):
    cursor = connection.cursor()
    cursor.execute(f"SELECT fullname FROM Doctors WHERE user_id = (SELECT user_id FROM Users WHERE username = '{fetch_doctor_fullname}')")
    result = cursor.fetchone()  # Fetch the result

    # Check if result is not None before subscripting
    if result is not None:
        fullname = result[0]  # Extract the fullname from the result
        return fullname
    else:
        return None  # Return None if no result is found


# Create main window
root = tk.Tk()
root.title("Doctor Home Page")
root.geometry("800x600")
root.configure(bg="white")

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Load images with specified size
button_size = (40, 40)
home_img = load_image("home.jpg", button_size)
list_of_patients_img = load_image("listofpatients.png", button_size)
profile_img = load_image("profile.jpg", button_size)
availability_status_img = load_image("availability.png", button_size)
logout_img = load_image("logout.jpg", button_size)
notification_img = load_image("bell.jpg", (30, 30))  # Load and resize the notification bell icon

# Left side menu
menu_frame = tk.Frame(root, bg="white")
menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Menu buttons with images and labels
def create_button(frame, image, text, command):
    btn = tk.Button(frame, image=image, command=command, bg="white", compound=tk.TOP)
    btn.pack(pady=5)
    label = tk.Label(frame, text=text, bg="white", font=("Arial", 10))
    label.pack()

create_button(menu_frame, home_img, "HOME", home_action)
create_button(menu_frame, list_of_patients_img, "LIST OF PATIENTS", list_of_patients_action)
create_button(menu_frame, profile_img, "PROFILE", profile_action)
create_button(menu_frame, availability_status_img, "AVAILABILITY STATUS", availability_status_action)
create_button(menu_frame, logout_img, "LOGOUT", logout_action)

# Function to fetch past and upcoming appointments
def fetch_appointments(connection, username):
    cursor = connection.cursor()

    # Fetch past appointments
    cursor.execute(f"""
    SELECT appointment_date, appointment_type
    FROM Appointments
    WHERE doctor_id = (SELECT doctor_id FROM Doctors WHERE user_id = (SELECT user_id FROM Users WHERE username = '{username}'))
    AND appointment_date < NOW()
    """)
    past_appointments = cursor.fetchall()

    # Fetch upcoming appointments
    cursor.execute(f"""
    SELECT appointment_date, appointment_type
    FROM Appointments
    WHERE doctor_id = (SELECT doctor_id FROM Doctors WHERE user_id = (SELECT user_id FROM Users WHERE username = '{username}'))
    AND appointment_date >= NOW()
    """)
    upcoming_appointments = cursor.fetchall()

    return past_appointments, upcoming_appointments

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Welcome text
welcome_label = tk.Label(main_frame, text="Welcome DR.LINKESH", font=("Arial", 24), bg="white")
welcome_label.pack(pady=20)

# Appointment history section
history_frame = tk.Frame(main_frame, bg="lightblue", padx=10, pady=10)
history_frame.pack(fill=tk.BOTH, expand=True)

past_appointments_label = tk.Label(history_frame, text="PAST APPOINTMENTS", bg="lightblue", font=("Arial", 14))
past_appointments_label.pack(fill=tk.X, pady=(0, 10))

# Past appointments list
past_appointments_list = tk.Listbox(history_frame)
past_appointments_list.pack(fill=tk.BOTH, expand=True)

# Upcoming appointments label
upcoming_appointments_label = tk.Label(history_frame, text="UPCOMING APPOINTMENTS", bg="lightblue", font=("Arial", 14))
upcoming_appointments_label.pack(fill=tk.X, pady=(10, 0))

# Upcoming appointments list
upcoming_appointments_list = tk.Listbox(history_frame)
upcoming_appointments_list.pack(fill=tk.BOTH, expand=True)

# Notification button with image
notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
notification_btn.place(x=760, y=20)

# Function to update appointments
def update_appointments(username):
    # Create database connection
    connection = create_connection()

    # Fetch and display appointments
    past_appointments, upcoming_appointments = fetch_appointments(connection, username)

    for appointment in past_appointments:
        past_appointments_list.insert(tk.END, f"{appointment[0]} - {appointment[1]}")

    for appointment in upcoming_appointments:
        upcoming_appointments_list.insert(tk.END, f"{appointment[0]} - {appointment[1]}")

    # Close database connection
    connection.close()

# Update appointments and fullname
def update_doctor_home(username):
    # Fetch doctor's fullname
    connection = create_connection()
    fullname = fetch_doctor_fullname(connection, username)
    welcome_label.config(text=f"Welcome {fullname}")

    # Update appointments
    update_appointments(username)

    # Close database connection
    connection.close()

# Example of how to fetch users
def fetch_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    print("Users retrieved successfully")
    for user in users:
        print(user)

# Call update function with the username
update_doctor_home("doctor_user")

root.mainloop()

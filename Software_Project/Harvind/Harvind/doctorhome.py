import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
import sys
import subprocess

# Database connection function
def get_doctor_fullname(doctor_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="calladoctor1234",
            database="calladoctor"
        )
        cursor = db.cursor()
        cursor.execute("SELECT fullname FROM doctors WHERE doctor_id = %s", (doctor_id,))
        result = cursor.fetchone()
        db.close()
        print(f"Doctor ID: {doctor_id}, Fullname: {result}")  # Debug print statement
        return result[0] if result else "Doctor"
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        return "Doctor"

# Function for button actions
def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def list_of_patients_action():
    root.destroy()
    subprocess.run(['python', 'listofpatient.py'])

def profile_action():
    messagebox.showinfo("Profile", "Profile Button Clicked")

def availability_status_action():
    messagebox.showinfo("Availability Status", "Availability Status Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

# Create main window
root = tk.Tk()
root.title("Doctor Home Page")
root.geometry("800x600")
root.configure(bg="white")

# Image file path
image_path = "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/Images/"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Load images with specified size
button_size = (40, 40)
home_img = load_image("home.png", button_size)
list_of_patients_img = load_image("listofpatients.png", button_size)
profile_img = load_image("profile.png", button_size)
availability_status_img = load_image("availability.png", button_size)
logout_img = load_image("logout.png", button_size)
notification_img = load_image("bell.png", (30, 30))  # Load and resize the notification bell icon

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

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Get doctor_id from command-line arguments
doctor_id = int(sys.argv[1])
doctor_fullname = get_doctor_fullname(doctor_id)

# Welcome text
welcome_label = tk.Label(main_frame, text=f"Welcome DR. {doctor_fullname}", font=("Arial", 24), bg="white")
welcome_label.pack(pady=20)

# Appointment history section
history_frame = tk.Frame(main_frame, bg="lightblue", padx=10, pady=10)
history_frame.pack(fill=tk.BOTH, expand=True)

past_appointments_label = tk.Label(history_frame, text="PAST APPOINTMENTS", bg="lightblue", font=("Arial", 14))
past_appointments_label.pack(fill=tk.X, pady=(0, 10))

# Past appointments list (placeholder)
past_appointments_list = tk.Listbox(history_frame)
past_appointments_list.pack(fill=tk.BOTH, expand=True)

upcoming_appointments_label = tk.Label(history_frame, text="UPCOMING APPOINTMENTS", bg="lightblue", font=("Arial", 14))
upcoming_appointments_label.pack(fill=tk.X, pady=(10, 0))

# Upcoming appointments list (placeholder)
upcoming_appointments_list = tk.Listbox(history_frame)
upcoming_appointments_list.pack(fill=tk.BOTH, expand=True)

# Notification button with image
notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
notification_btn.place(x=760, y=20)

root.mainloop()

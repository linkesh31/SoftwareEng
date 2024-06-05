import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Function for button actions
def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def patients_management_action():
    messagebox.showinfo("Patients Management", "Patients Management Button Clicked")

def doctors_management_action():
    messagebox.showinfo("Doctors Management", "Doctors Management Button Clicked")

def clinics_management_action():
    messagebox.showinfo("Clinics Management", "Clinics Management Button Clicked")

def appointment_management_action():
    messagebox.showinfo("Appointment Management", "Appointment Management Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

# Create main window
root = tk.Tk()
root.title("Admin Home Page")
root.geometry("800x600")
root.configure(bg="white")

# Image file path
image_path = "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Images/"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Load images with specified size
button_size = (40, 40)
home_img = load_image("home.png", button_size)
patients_management_img = load_image("patients_management.png", button_size)
doctors_management_img = load_image("doctors_management.png", button_size)
clinics_management_img = load_image("clinics_management.png", button_size)
appointment_management_img = load_image("appointments_management.png", button_size)
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
create_button(menu_frame, patients_management_img, "PATIENTS MANAGEMENT", patients_management_action)
create_button(menu_frame, doctors_management_img, "DOCTORS MANAGEMENT", doctors_management_action)
create_button(menu_frame, clinics_management_img, "CLINICS MANAGEMENT", clinics_management_action)
create_button(menu_frame, appointment_management_img, "APPOINTMENT MANAGEMENT", appointment_management_action)
create_button(menu_frame, logout_img, "LOGOUT", logout_action)

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Welcome text
welcome_label = tk.Label(main_frame, text="Welcome ADMIN", font=("Arial", 24), bg="white")
welcome_label.pack(pady=20)

# Registered Clinics and Doctors section in a table format
stats_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
stats_frame.pack(fill=tk.BOTH, expand=True)

# Table headers
total_registered_clinics_label = tk.Label(stats_frame, text="Total registered Clinics", font=("Arial", 14), bg="white", borderwidth=2, relief="solid")
total_registered_clinics_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

total_registered_doctors_label = tk.Label(stats_frame, text="Total registered Doctors", font=("Arial", 14), bg="white", borderwidth=2, relief="solid")
total_registered_doctors_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Table values
total_registered_clinics_count = tk.Label(stats_frame, text="11", font=("Arial", 24), bg="white", borderwidth=2, relief="solid")
total_registered_clinics_count.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

total_registered_doctors_count = tk.Label(stats_frame, text="24", font=("Arial", 24), bg="white", borderwidth=2, relief="solid")
total_registered_doctors_count.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Set grid column weights for equal column width
stats_frame.grid_columnconfigure(0, weight=1)
stats_frame.grid_columnconfigure(1, weight=1)

# Notification button with image
notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
notification_btn.place(x=760, y=20)

root.mainloop()
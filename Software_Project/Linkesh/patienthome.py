import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys

# Get patient's full name from command line argument
if len(sys.argv) > 1:
    patient_fullname = sys.argv[1]
else:
    patient_fullname = "PATIENT"

# Function for button actions
def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def search_view_clinic_action():
    messagebox.showinfo("Search/View Clinic", "Search/View Clinic Button Clicked")

def send_request_to_doctor_action():
    messagebox.showinfo("Send Request to Doctor", "Send Request to Doctor Button Clicked")

def profile_action():
    messagebox.showinfo("Profile", "Profile Button Clicked")

def appointment_summary_action():
    messagebox.showinfo("Appointment Summary", "Appointment Summary Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

# Create main window
root = tk.Tk()
root.title("Appointment System")
root.geometry("800x600")
root.configure(bg="white")

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Load images with specified size
button_size = (40, 40)
home_img = load_image("home.jpg", button_size)
search_view_clinic_img = load_image("search.jpg", button_size)
send_request_to_doctor_img = load_image("sendrequest.jpg", button_size)
profile_img = load_image("profile.jpg", button_size)
appointment_summary_img = load_image("appointment.jpg", button_size)
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
create_button(menu_frame, search_view_clinic_img, "SEARCH/VIEW CLINIC", search_view_clinic_action)
create_button(menu_frame, send_request_to_doctor_img, "SEND REQUEST TO DOCTOR", send_request_to_doctor_action)
create_button(menu_frame, profile_img, "PROFILE", profile_action)
create_button(menu_frame, appointment_summary_img, "APPOINTMENT SUMMARY", appointment_summary_action)
create_button(menu_frame, logout_img, "LOGOUT", logout_action)

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Welcome text
welcome_label = tk.Label(main_frame, text=f"Welcome {patient_fullname}", font=("Arial", 24), bg="white")
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

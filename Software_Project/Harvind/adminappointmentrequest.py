import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import os
import subprocess
import mysql.connector
import sys

# Get clinic admin's clinic ID and full name from command line arguments
if len(sys.argv) > 2:
    clinic_id = sys.argv[1]
    admin_fullname = sys.argv[2]
else:
    clinic_id = "Unknown Clinic"
    admin_fullname = "ADMIN"

# Function to retrieve appointment requests
def get_appointment_requests(clinic_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        query = """
        SELECT a.appointment_id, p.fullname, a.appointment_date, a.appointment_time, d.fullname
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.clinic_id = %s AND a.appointment_request_status = 'pending'
        """
        cursor.execute(query, (clinic_id,))
        appointment_requests = cursor.fetchall()
        connection.close()
        return appointment_requests
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# Function to update appointment request status
def update_appointment_status(appointment_id, status):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        query = "UPDATE appointments SET appointment_request_status = %s WHERE appointment_id = %s"
        cursor.execute(query, (status, appointment_id))
        connection.commit()
        connection.close()
        refresh_appointment_requests()
        messagebox.showinfo("Success", f"Appointment {status} successfully")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to refresh the appointment requests table
def refresh_appointment_requests():
    for item in appointment_table.get_children():
        appointment_table.delete(item)
    appointment_requests = get_appointment_requests(clinic_id)
    for request in appointment_requests:
        appointment_table.insert('', 'end', values=request)

# Function for button actions
def home_action():
    root.destroy()
    subprocess.run(['python', 'adminclinichome.py', clinic_id, admin_fullname])

def patients_management_action():
    root.destroy()
    subprocess.run(['python', 'patientsmanagement.py', clinic_id, admin_fullname])

def doctors_management_action():
    root.destroy()
    subprocess.run(['python', 'doctorsmanagement.py', clinic_id, admin_fullname])

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

# Create main window
root = tk.Tk()
root.title(f"Admin Appointment Requests - {clinic_id}")
root.geometry("1300x800")
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
patients_management_img = load_image("patients_management.png", button_size)
doctors_management_img = load_image("doctors_management.png", button_size)
appointment_management_img = load_image("appointments_management.png", button_size)
logout_img = load_image("logout.png", button_size)
notification_img = load_image("bell.png", (30, 30))

# Left side menu
menu_frame = tk.Frame(root, bg="#E6E6FA")
menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Menu buttons with images and labels
def create_button(frame, image, text, command):
    button_frame = tk.Frame(frame, bg="#E6E6FA")
    button_frame.pack(fill=tk.X, pady=5, padx=5)
    btn = tk.Button(button_frame, image=image, command=command, bg="white", compound=tk.TOP)
    btn.pack(pady=0)
    label = tk.Label(button_frame, text=text, bg="#E6E6FA", font=("Arial", 12, "bold"))
    label.pack(pady=5)
    return button_frame

create_button(menu_frame, home_img, "HOME", home_action)
create_button(menu_frame, appointment_management_img, "APPOINTMENT REQUESTS", None)
create_button(menu_frame, patients_management_img, "PATIENTS MANAGEMENT", patients_management_action)
create_button(menu_frame, doctors_management_img, "DOCTORS MANAGEMENT", doctors_management_action)

# Logout button at the bottom
logout_frame = tk.Frame(menu_frame, bg="#E6E6FA")
logout_frame.pack(fill=tk.X, pady=5, padx=5)
logout_btn = tk.Button(logout_frame, image=logout_img, command=logout_action, bg="white", bd=0)
logout_btn.pack(pady=0)
logout_label = tk.Label(logout_frame, text="LOGOUT", bg="#E6E6FA", font=("Arial", 12, "bold"))
logout_label.pack(pady=5)

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Welcome text
welcome_label = tk.Label(main_frame, text=f"Welcome {admin_fullname}", font=("Arial", 24), bg="white")
welcome_label.pack(pady=20)

# Table title
table_title_label = tk.Label(main_frame, text="Appointment Request From Patients", font=("Arial", 18), bg="white")
table_title_label.pack(pady=10)

# Appointment requests table
columns = ("appointment_id", "patient_name", "appointment_date", "appointment_time", "doctor_name")
appointment_table = ttk.Treeview(main_frame, columns=columns, show='headings')
appointment_table.heading("appointment_id", text="ID")
appointment_table.heading("patient_name", text="Patient Name")
appointment_table.heading("appointment_date", text="Date")
appointment_table.heading("appointment_time", text="Time")
appointment_table.heading("doctor_name", text="Doctor Name")
appointment_table.column("appointment_id", anchor='center')
appointment_table.column("patient_name", anchor='center')
appointment_table.column("appointment_date", anchor='center')
appointment_table.column("appointment_time", anchor='center')
appointment_table.column("doctor_name", anchor='center')
appointment_table.pack(fill=tk.BOTH, expand=True)

# Add scrollbars to the table
scrollbar_x = tk.Scrollbar(appointment_table, orient=tk.HORIZONTAL, command=appointment_table.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
scrollbar_y = tk.Scrollbar(appointment_table, orient=tk.VERTICAL, command=appointment_table.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
appointment_table.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

# Center the table
appointment_table.pack(expand=True, fill=tk.BOTH)

# Button frame
button_frame = tk.Frame(main_frame, bg="white")
button_frame.pack(pady=10)

# Accept and Reject buttons
def accept_appointment():
    selected_item = appointment_table.selection()
    if selected_item:
        appointment_id = appointment_table.item(selected_item)["values"][0]
        update_appointment_status(appointment_id, 'accepted')

def reject_appointment():
    selected_item = appointment_table.selection()
    if selected_item:
        appointment_id = appointment_table.item(selected_item)["values"][0]
        update_appointment_status(appointment_id, 'rejected')

accept_btn = tk.Button(button_frame, text="Accept", command=accept_appointment, bg="green", fg="white", font=("Arial", 12, "bold"))
accept_btn.pack(side=tk.LEFT, padx=10)

reject_btn = tk.Button(button_frame, text="Reject", command=reject_appointment, bg="red", fg="white", font=("Arial", 12, "bold"))
reject_btn.pack(side=tk.LEFT, padx=10)

# Notification button with image
notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
notification_btn.place(x=1160, y=20)

# Initialize appointment requests in the table
refresh_appointment_requests()

root.mainloop()

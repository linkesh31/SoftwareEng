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
    admin_fullname = ' '.join(sys.argv[2:])  # Join the rest as admin_fullname
else:
    clinic_id = "Unknown Clinic"
    admin_fullname = "ADMIN"

# Function to retrieve clinic details
def get_clinic_details(clinic_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT clinic_name, address FROM clinics WHERE clinic_id=%s", (clinic_id,))
        clinic_details = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM doctors WHERE clinic_id=%s", (clinic_id,))
        total_doctors = cursor.fetchone()[0]

        connection.close()

        if clinic_details:
            return clinic_details[0], clinic_details[1], total_doctors
        else:
            return "Unknown Clinic", "Unknown Address", 0
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        return "Unknown Clinic", "Unknown Address", 0

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
        row_id = appointment_table.insert('', 'end', values=(request[1], request[2], request[3], request[4]))
        appointment_ids[row_id] = request[0]  # Store appointment_id in dictionary with row_id as key

# Function for button actions
def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def appointment_management_action():
    subprocess.run(['python', 'adminappointmentschedule.py', clinic_id, admin_fullname])

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

def add_doctor_action():
    root.destroy()
    subprocess.run(['python', 'adddoctor.py', clinic_id, admin_fullname])

def delete_doctor_action():
    root.destroy()
    subprocess.run(['python', 'deletedoctor.py', clinic_id, admin_fullname])

# Function to show options on hover
def show_doctor_management_menu(event):
    doctor_management_menu.post(event.x_root, event.y_root)
    root.after_cancel(hide_menu_job)

# Function to hide options when not hovering
def hide_doctor_management_menu(event):
    global hide_menu_job
    hide_menu_job = root.after(500, doctor_management_menu.unpost)

# Retrieve clinic details
clinic_name, clinic_address, total_doctors = get_clinic_details(clinic_id)

# Create main window
root = tk.Tk()
root.title(f"Clinic Admin Home Page - {clinic_name}")
root.geometry("1400x800")
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
patients_management_img = load_image("patients_management.png", button_size)
doctors_management_img = load_image("doctors_management.png", button_size)
appointment_management_img = load_image("appointments_management.png", button_size)
logout_img = load_image("logout.jpg", button_size)

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

# Doctor Management button
doctor_management_button_frame = create_button(menu_frame, doctors_management_img, "DOCTORS MANAGEMENT", None)

# Create hover menu for Doctor Management
doctor_management_menu = tk.Menu(root, tearoff=0, bg="lightgrey", font=("Arial", 10))
doctor_management_menu.add_command(label="Add Doctor", command=add_doctor_action)
doctor_management_menu.add_command(label="Delete Doctor", command=delete_doctor_action)

# Bind hover event to Doctor Management button and label
doctor_management_button = doctor_management_button_frame.winfo_children()[0]
doctor_management_label = doctor_management_button_frame.winfo_children()[1]
doctor_management_button.bind("<Enter>", show_doctor_management_menu)
doctor_management_button.bind("<Leave>", hide_doctor_management_menu)
doctor_management_label.bind("<Enter>", show_doctor_management_menu)
doctor_management_label.bind("<Leave>", hide_doctor_management_menu)

# Bind hover event to menu to prevent it from hiding
doctor_management_menu.bind("<Enter>", lambda event: root.after_cancel(hide_menu_job))
doctor_management_menu.bind("<Leave>", hide_doctor_management_menu)

# Create remaining buttons
create_button(menu_frame, appointment_management_img, "APPOINTMENT SCHEDULE", appointment_management_action)

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

# Clinic details
clinic_details_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
clinic_details_frame.pack(fill=tk.BOTH, expand=True)

clinic_name_label = tk.Label(clinic_details_frame, text=f"Clinic Name: {clinic_name}", font=("Arial", 18), bg="white")
clinic_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

address_label = tk.Label(clinic_details_frame, text=f"Address: {clinic_address}", font=("Arial", 18), bg="white")
address_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

total_doctors_label = tk.Label(clinic_details_frame, text=f"Total registered doctors: {total_doctors}", font=("Arial", 18), bg="white")
total_doctors_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Table title
table_title_frame = tk.Frame(clinic_details_frame, bg="white")
table_title_frame.grid(row=3, column=0, columnspan=2)
table_title_label = tk.Label(table_title_frame, text="Appointment Request From Patients", font=("Arial", 18), bg="white")
table_title_label.pack(pady=10)

# Appointment requests table
columns = ("patient_name", "appointment_date", "appointment_time", "doctor_name")
appointment_table = ttk.Treeview(clinic_details_frame, columns=columns, show='headings')
appointment_table.heading("patient_name", text="Patient Name")
appointment_table.heading("appointment_date", text="Date")
appointment_table.heading("appointment_time", text="Time")
appointment_table.heading("doctor_name", text="Doctor Name")
appointment_table.column("patient_name", anchor='center')
appointment_table.column("appointment_date", anchor='center')
appointment_table.column("appointment_time", anchor='center')
appointment_table.column("doctor_name", anchor='center')
appointment_table.grid(row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

# Dictionary to store appointment_ids
appointment_ids = {}

# Add scrollbars to the table
scrollbar_y = tk.Scrollbar(clinic_details_frame, orient=tk.VERTICAL, command=appointment_table.yview)
scrollbar_y.grid(row=4, column=2, sticky="ns")
scrollbar_x = tk.Scrollbar(clinic_details_frame, orient=tk.HORIZONTAL, command=appointment_table.xview)
scrollbar_x.grid(row=5, column=0, sticky="ew", columnspan=2)

appointment_table.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# Make the table expand to fit the frame
clinic_details_frame.grid_rowconfigure(4, weight=1)
clinic_details_frame.grid_columnconfigure(0, weight=1)

# Button frame
button_frame = tk.Frame(clinic_details_frame, bg="white")
button_frame.grid(row=6, column=0, padx=10, pady=10, sticky="w")

# Accept and Reject buttons
def accept_appointment():
    selected_item = appointment_table.selection()
    if selected_item:
        row_id = selected_item[0]
        appointment_id = appointment_ids[row_id]
        update_appointment_status(appointment_id, 'accepted')
    else:
        messagebox.showerror("Error", "Please select an appointment to accept.")

def reject_appointment():
    selected_item = appointment_table.selection()
    if selected_item:
        row_id = selected_item[0]
        appointment_id = appointment_ids[row_id]
        update_appointment_status(appointment_id, 'rejected')
    else:
        messagebox.showerror("Error", "Please select an appointment to reject.")

accept_btn = tk.Button(button_frame, text="Accept", command=accept_appointment, bg="green", fg="white", font=("Arial", 12, "bold"))
accept_btn.pack(side=tk.LEFT, padx=10)

reject_btn = tk.Button(button_frame, text="Reject", command=reject_appointment, bg="red", fg="white", font=("Arial", 12, "bold"))
reject_btn.pack(side=tk.LEFT, padx=10)

# Initialize appointment requests in the table
refresh_appointment_requests()

# Initialize hide menu job
hide_menu_job = None

root.mainloop()

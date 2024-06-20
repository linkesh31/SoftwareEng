import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import mysql.connector
import customtkinter as ctk

# Get patient_id and patient's full name from command line arguments
if len(sys.argv) > 2:
    patient_id = int(sys.argv[1])
    patient_fullname = sys.argv[2]
else:
    patient_id = 1  # Default patient_id
    patient_fullname = "PATIENT"

# Database connection details
db_config = {
    'user': 'root',
    'password': 'calladoctor1234',
    'host': 'localhost',
    'database': 'calladoctor'
}

# Fetch appointments based on patient_id
def fetch_appointments(patient_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT a.appointment_date, a.appointment_time, a.reason, d.fullname AS doctor_name, c.clinic_name, a.appointment_request_status
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            JOIN clinics c ON a.clinic_id = c.clinic_id
            WHERE a.patient_id = %s AND a.appointment_request_status IN ('accepted', 'rejected')
            ORDER BY a.appointment_date ASC
        """, (patient_id,))
        approved_requests = cursor.fetchall()

        cursor.execute("""
            SELECT a.appointment_date, a.appointment_time, a.reason, d.fullname AS doctor_name, c.clinic_name
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            JOIN clinics c ON a.clinic_id = c.clinic_id
            WHERE a.patient_id = %s AND a.appointment_request_status = 'pending'
            ORDER BY a.appointment_date ASC
        """, (patient_id,))
        pending_requests = cursor.fetchall()

        cursor.close()
        connection.close()

        return approved_requests, pending_requests
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
        return [], []

def refresh_appointments():
    approved_requests, pending_requests = fetch_appointments(patient_id)
    for widget in approved_requests_frame.winfo_children():
        widget.destroy()
    for widget in pending_requests_frame.winfo_children():
        widget.destroy()
    for col in range(6):
        approved_requests_frame.grid_columnconfigure(col, weight=1)
    for col in range(6):
        pending_requests_frame.grid_columnconfigure(col, weight=1)

    approved_columns = ["Date", "Time", "Reason", "Doctor", "Clinic", "Status"]
    for col in approved_columns:
        header = ctk.CTkLabel(approved_requests_frame, text=col, font=("Arial", 14, "bold"), fg_color="lightblue")
        header.grid(row=0, column=approved_columns.index(col), sticky="nsew")

    for i, request in enumerate(approved_requests):
        for j, value in enumerate(request):
            label = ctk.CTkLabel(approved_requests_frame, text=value, font=("Arial", 12), fg_color="white")
            label.grid(row=i+1, column=j, sticky="nsew")

    pending_columns = ["Date", "Time", "Reason", "Doctor", "Clinic", "Action"]
    for col in pending_columns:
        header = ctk.CTkLabel(pending_requests_frame, text=col, font=("Arial", 14, "bold"), fg_color="lightblue")
        header.grid(row=0, column=pending_columns.index(col), sticky="nsew")

    for i, request in enumerate(pending_requests):
        for j, value in enumerate(request):
            label = ctk.CTkLabel(pending_requests_frame, text=value, font=("Arial", 12), fg_color="white")
            label.grid(row=i+1, column=j, sticky="nsew")
        delete_button = ctk.CTkButton(pending_requests_frame, text="Delete", command=lambda req=request: confirm_delete_appointment(req[0]), fg_color="red", text_color="white", font=("Arial", 10))
        delete_button.grid(row=i+1, column=len(request), sticky="nsew")
        pending_requests_frame.grid_columnconfigure(len(request), weight=1)

def confirm_delete_appointment(appointment_date):
    response = messagebox.askyesno("Delete Confirmation", "Do you want to delete this appointment?")
    if response:
        delete_appointment(appointment_date)

def delete_appointment(appointment_date):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE appointments
            SET appointment_request_status = 'cancelled'
            WHERE patient_id = %s AND appointment_date = %s
        """, (patient_id, appointment_date))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Appointment request cancelled successfully!")
        refresh_appointments()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Failed to cancel the appointment request: {e}")

def appointment_book_action():
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/request_appointment_patient.py" {patient_id} {patient_fullname}')

def profile_action():
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/patientprofile.py" {patient_id} {patient_fullname}')

def appointment_summary_action():
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/patient_appointmentsummary.py" {patient_id} {patient_fullname}')

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

# Initialize main window
ctk.set_appearance_mode("light")  # Modes: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Appointment System")
root.geometry("1000x700")
root.configure(fg_color="#AED6F1")  # Set the main window background color

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=img, size=size)

# Load images with specified size
button_size = (40, 40)
appointment_book_img = load_image("search.png", button_size)
profile_img = load_image("profile.png", button_size)
appointment_summary_img = load_image("appointment.png", button_size)
logout_img = load_image("logout.png", button_size)

# Left side menu
menu_frame = ctk.CTkFrame(root, fg_color="#E6E6FA")
menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Menu buttons with images and labels
def create_button(frame, image, text, command):
    button_frame = ctk.CTkFrame(frame, fg_color="#E6E6FA")
    button_frame.pack(fill=tk.X, pady=5, padx=5)
    btn = ctk.CTkButton(button_frame, image=image, command=command, fg_color="white", hover_color="#AED6F1", text="")
    btn.pack(pady=0)
    label = ctk.CTkLabel(button_frame, text=text, fg_color="#E6E6FA", font=("Arial", 12, "bold"))
    label.pack(pady=5)
    return button_frame

create_button(menu_frame, appointment_book_img, "BOOK APPOINTMENT", appointment_book_action)
create_button(menu_frame, profile_img, "PROFILE", profile_action)
create_button(menu_frame, appointment_summary_img, "APPOINTMENT SUMMARY", appointment_summary_action)

# Logout button at the bottom
logout_frame = ctk.CTkFrame(menu_frame, fg_color="#E6E6FA")
logout_frame.pack(fill=tk.X, pady=5, padx=5)
logout_btn = ctk.CTkButton(logout_frame, image=logout_img, command=logout_action, fg_color="white", hover_color="#AED6F1", text="")
logout_btn.pack(pady=0)
logout_label = ctk.CTkLabel(logout_frame, text="LOGOUT", fg_color="#E6E6FA", font=("Arial", 12, "bold"))
logout_label.pack(pady=5)

# Main content area
main_frame = ctk.CTkFrame(root, fg_color="#AED6F1")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Welcome text
welcome_label = ctk.CTkLabel(main_frame, text=f"Welcome {patient_fullname}", font=("Arial", 24), fg_color="#AED6F1")
welcome_label.pack(pady=20)

# Approved/Rejected Requests
approved_requests_label = ctk.CTkLabel(main_frame, text="APPROVED/REJECTED APPOINTMENT REQUESTS", fg_color="lightblue", font=("Arial", 18))
approved_requests_label.pack(fill=tk.X, pady=(0, 10))

approved_requests_frame = ctk.CTkFrame(main_frame, fg_color="white")
approved_requests_frame.pack(fill=tk.BOTH, expand=True)

# Pending Requests
pending_requests_label = ctk.CTkLabel(main_frame, text="PENDING APPOINTMENT REQUESTS", fg_color="lightblue", font=("Arial", 18))
pending_requests_label.pack(fill=tk.X, pady=(10, 0))

pending_requests_frame = ctk.CTkFrame(main_frame, fg_color="white")
pending_requests_frame.pack(fill=tk.BOTH, expand=True)

refresh_appointments()
root.mainloop()

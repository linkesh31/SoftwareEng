import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

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
        header = tk.Label(approved_requests_frame, text=col, font=("Arial", 10, "bold"), bg="lightblue")
        header.grid(row=0, column=approved_columns.index(col), sticky="nsew")

    for i, request in enumerate(approved_requests):
        for j, value in enumerate(request):
            label = tk.Label(approved_requests_frame, text=value, font=("Arial", 10), bg="white")
            label.grid(row=i+1, column=j, sticky="nsew")

    pending_columns = ["Date", "Time", "Reason", "Doctor", "Clinic", "Action"]
    for col in pending_columns:
        header = tk.Label(pending_requests_frame, text=col, font=("Arial", 10, "bold"), bg="lightblue")
        header.grid(row=0, column=pending_columns.index(col), sticky="nsew")

    for i, request in enumerate(pending_requests):
        for j, value in enumerate(request):
            label = tk.Label(pending_requests_frame, text=value, font=("Arial", 10), bg="white")
            label.grid(row=i+1, column=j, sticky="nsew")
        delete_button = tk.Button(pending_requests_frame, text="Delete", command=lambda req=request: confirm_delete_appointment(req[0]), bg="red", fg="white", font=("Arial", 10))
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

def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def appointment_book_action():
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/request_appointment_patient.py" {patient_id} {patient_fullname}')

def profile_action():
    messagebox.showinfo("Profile", "Profile Button Clicked")

def appointment_summary_action():
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/patient_appointmentsummary.py" {patient_id} {patient_fullname}')

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

root = tk.Tk()
root.title("Appointment System")
root.geometry("800x600")
root.configure(bg="white")

image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

button_size = (40, 40)
home_img = load_image("home.jpg", button_size)
appointment_book_img = load_image("search.jpg", button_size)
profile_img = load_image("profile.jpg", button_size)
appointment_summary_img = load_image("appointment.jpg", button_size)
logout_img = load_image("logout.jpg", button_size)
notification_img = load_image("bell.jpg", (30, 30))

menu_frame = tk.Frame(root, bg="white")
menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

def create_button(frame, image, text, command):
    btn = tk.Button(frame, image=image, command=command, bg="white", compound=tk.TOP)
    btn.pack(pady=5)
    label = tk.Label(frame, text=text, bg="white", font=("Arial", 10))
    label.pack()

create_button(menu_frame, home_img, "HOME", home_action)
create_button(menu_frame, appointment_book_img, "BOOK APPOINTMENT", appointment_book_action)
create_button(menu_frame, profile_img, "PROFILE", profile_action)
create_button(menu_frame, appointment_summary_img, "APPOINTMENT SUMMARY", appointment_summary_action)
create_button(menu_frame, logout_img, "LOGOUT", logout_action)

main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

welcome_label = tk.Label(main_frame, text=f"Welcome {patient_fullname}", font=("Arial", 24), bg="white")
welcome_label.pack(pady=20)

approved_requests_label = tk.Label(main_frame, text="APPROVED/REJECTED APPOINTMENT REQUESTS", bg="lightblue", font=("Arial", 14))
approved_requests_label.pack(fill=tk.X, pady=(0, 10))

approved_requests_frame = tk.Frame(main_frame, bg="white")
approved_requests_frame.pack(fill=tk.BOTH, expand=True)

pending_requests_label = tk.Label(main_frame, text="PENDING APPOINTMENT REQUESTS", bg="lightblue", font=("Arial", 14))
pending_requests_label.pack(fill=tk.X, pady=(10, 0))

pending_requests_frame = tk.Frame(main_frame, bg="white")
pending_requests_frame.pack(fill=tk.BOTH, expand=True)

refresh_appointments()
root.mainloop()

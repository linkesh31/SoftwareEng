import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import subprocess
import sys
from tkinter import ttk

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

def fetch_clinics():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT clinic_id, clinic_name FROM clinics WHERE is_approved = 1")
        clinics = cursor.fetchall()
        cursor.close()
        connection.close()
        return {clinic_name: clinic_id for clinic_id, clinic_name in clinics}
    except Error as e:
        print(f"The error '{e}' occurred")
        return {}

def fetch_doctors(clinic_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT doctor_id, fullname FROM doctors WHERE clinic_id = %s", (clinic_id,))
        doctors = cursor.fetchall()
        cursor.close()
        connection.close()
        return doctors
    except Error as e:
        print(f"The error '{e}' occurred")
        return []

def on_clinic_select(event):
    selected_clinic_name = clinic_var.get()
    selected_clinic_id = clinics[selected_clinic_name]
    doctors = fetch_doctors(selected_clinic_id)
    doctor_var.set('')
    doctor_menu['values'] = [doctor_name for doctor_id, doctor_name in doctors]
    doctor_dict.clear()
    doctor_dict.update({doctor_name: doctor_id for doctor_id, doctor_name in doctors})

def send_appointment_request():
    clinic_name = clinic_var.get()
    clinic_id = clinics[clinic_name]
    doctor_name = doctor_var.get()
    doctor_id = doctor_dict.get(doctor_name)
    reason = reason_entry.get("1.0", tk.END).strip()
    date = cal.get_date()
    hour = hour_var.get()
    minute = minute_var.get()
    time = f"{hour}:{minute}"

    if not clinic_id or not doctor_id or not reason or not date or not time:
        messagebox.showerror("Error", "All fields are required")
        return

    # Convert date format from 'mm/dd/yy' to 'yyyy-mm-dd'
    date_obj = datetime.strptime(date, '%m/%d/%y')
    formatted_date = date_obj.strftime('%Y-%m-%d')

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO appointments (clinic_id, doctor_id, patient_id, appointment_date, appointment_time, reason, appointment_request_status)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        """, (clinic_id, doctor_id, patient_id, formatted_date, time, reason))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Appointment request sent successfully!")
        go_back_to_patient_home()  # Go back to patient home after sending the request
    except Error as e:
        messagebox.showerror("Error", f"Failed to send appointment request: {e}")

def go_back_to_patient_home():
    root.destroy()
    subprocess.run(['python', 'patienthome.py', str(patient_id), patient_fullname])

# Create main window
root = tk.Tk()
root.title("Request Appointment")
root.geometry("600x500")

clinics = fetch_clinics()
doctor_dict = {}

# Clinic dropdown
clinic_label = tk.Label(root, text="Clinics Available:")
clinic_label.pack()
clinic_var = tk.StringVar()
clinic_menu = ttk.Combobox(root, textvariable=clinic_var, width=50)
clinic_menu['values'] = list(clinics.keys())
clinic_menu.bind("<<ComboboxSelected>>", on_clinic_select)
clinic_menu.pack()

# Doctor dropdown
doctor_label = tk.Label(root, text="Doctors:")
doctor_label.pack()
doctor_var = tk.StringVar()
doctor_menu = ttk.Combobox(root, textvariable=doctor_var, width=50)
doctor_menu.pack()

# Reason text box
reason_label = tk.Label(root, text="Reason:")
reason_label.pack()
reason_entry = tk.Text(root, height=4, width=50)
reason_entry.pack()

# Date picker
date_label = tk.Label(root, text="Date:")
date_label.pack()
cal = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
cal.pack()

# Time picker
time_label = tk.Label(root, text="Select Time:")
time_label.pack()

time_frame = tk.Frame(root)
time_frame.pack()

hour_var = tk.StringVar()
hour_menu = ttk.Combobox(time_frame, textvariable=hour_var, width=3)
hour_menu['values'] = [f"{hour:02d}" for hour in range(9, 18)]
hour_menu.pack(side=tk.LEFT, padx=5)

minute_var = tk.StringVar()
minute_menu = ttk.Combobox(time_frame, textvariable=minute_var, width=3)
minute_menu['values'] = ["00", "15", "30", "45"]
minute_menu.pack(side=tk.LEFT, padx=5)

# Send appointment request button
send_request_button = tk.Button(root, text="Send appointment request", command=send_appointment_request)
send_request_button.pack(pady=10)

# Back button
back_button = tk.Button(root, text="Back", command=go_back_to_patient_home)
back_button.pack(pady=5)

root.mainloop()

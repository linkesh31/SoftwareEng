import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os
import sys

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

def fetch_appointments(patient_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch past appointments
        cursor.execute("""
            SELECT a.appointment_date, a.appointment_time, a.reason, d.fullname AS doctor_name, c.clinic_name, IFNULL(pr.medical_report, 'N/A')
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            JOIN clinics c ON a.clinic_id = c.clinic_id
            LEFT JOIN prescriptions pr ON a.appointment_id = pr.appointment_id
            WHERE a.patient_id = %s AND a.treatment_status = 'done'
            ORDER BY a.appointment_date DESC
        """, (patient_id,))
        past_appointments = cursor.fetchall()

        # Fetch upcoming appointments
        cursor.execute("""
            SELECT a.appointment_date, a.appointment_time, a.reason, d.fullname AS doctor_name, c.clinic_name, 'N/A' AS prescriptions
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            JOIN clinics c ON a.clinic_id = c.clinic_id
            WHERE a.patient_id = %s AND a.treatment_status = 'pending' AND a.appointment_request_status = 'accepted'
            ORDER BY a.appointment_date ASC
        """, (patient_id,))
        upcoming_appointments = cursor.fetchall()

        cursor.close()
        connection.close()

        return past_appointments, upcoming_appointments
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
        return [], []

def back_action():
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/patienthome.py" {patient_id} {patient_fullname}')

root = tk.Tk()
root.title("Appointment System")
root.geometry("800x800")
root.configure(bg="white")

main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

history_frame = tk.Frame(main_frame, bg="lightblue", padx=10, pady=10)
history_frame.pack(fill=tk.BOTH, expand=True)

past_appointments_label = tk.Label(history_frame, text="PAST APPOINTMENTS", bg="lightblue", font=("Arial", 14))
past_appointments_label.pack(fill=tk.X, pady=(0, 10))

past_appointments_tree = ttk.Treeview(history_frame, columns=("date", "time", "reason", "doctor", "clinic", "prescriptions"), show='headings')
past_appointments_tree.heading("date", text="Date")
past_appointments_tree.heading("time", text="Time")
past_appointments_tree.heading("reason", text="Reason")
past_appointments_tree.heading("doctor", text="Doctor")
past_appointments_tree.heading("clinic", text="Clinic")
past_appointments_tree.heading("prescriptions", text="Prescriptions")
past_appointments_tree.pack(fill=tk.BOTH, expand=True)

for col in ("date", "time", "reason", "doctor", "clinic", "prescriptions"):
    past_appointments_tree.column(col, anchor="center", width=100, stretch=tk.YES)

upcoming_appointments_label = tk.Label(history_frame, text="UPCOMING APPOINTMENTS", bg="lightblue", font=("Arial", 14))
upcoming_appointments_label.pack(fill=tk.X, pady=(10, 0))

upcoming_appointments_tree = ttk.Treeview(history_frame, columns=("date", "time", "reason", "doctor", "clinic"), show='headings')
upcoming_appointments_tree.heading("date", text="Date")
upcoming_appointments_tree.heading("time", text="Time")
upcoming_appointments_tree.heading("reason", text="Reason")
upcoming_appointments_tree.heading("doctor", text="Doctor")
upcoming_appointments_tree.heading("clinic", text="Clinic")
upcoming_appointments_tree.pack(fill=tk.BOTH, expand=True)

for col in ("date", "time", "reason", "doctor", "clinic"):
    upcoming_appointments_tree.column(col, anchor="center", width=100, stretch=tk.YES)

# Fetch appointment data for the specific patient
past_appointments, upcoming_appointments = fetch_appointments(patient_id)

# Insert data into the tables
for appointment in past_appointments:
    past_appointments_tree.insert("", "end", values=appointment)

for appointment in upcoming_appointments:
    upcoming_appointments_tree.insert("", "end", values=appointment)

back_button = tk.Button(main_frame, text="Back", command=back_action, bg="white", font=("Arial", 12))
back_button.pack(pady=10)

root.mainloop()

import customtkinter as ctk
from tkinter import ttk
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

# Create main window
ctk.set_appearance_mode("light")  # Modes: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Appointment System")
root.geometry("800x700")
root.configure(fg_color="white")

main_frame = ctk.CTkFrame(root, fg_color="white")
main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

history_frame = ctk.CTkFrame(main_frame, fg_color="lightblue", corner_radius=10)
history_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

past_appointments_label = ctk.CTkLabel(history_frame, text="PAST APPOINTMENTS", fg_color="lightblue", font=("Arial", 18))
past_appointments_label.pack(fill=ctk.X, pady=(0, 10))

# Style for Treeview
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
style.configure("Treeview", font=("Arial", 12), rowheight=25)  # Set font size for the table contents

past_appointments_tree = ttk.Treeview(history_frame, columns=("date", "time", "reason", "doctor", "clinic", "prescriptions"), show='headings')
past_appointments_tree.heading("date", text="Date")
past_appointments_tree.heading("time", text="Time")
past_appointments_tree.heading("reason", text="Reason")
past_appointments_tree.heading("doctor", text="Doctor")
past_appointments_tree.heading("clinic", text="Clinic")
past_appointments_tree.heading("prescriptions", text="Prescriptions")
past_appointments_tree.pack(fill=ctk.BOTH, expand=True)

for col in ("date", "time", "reason", "doctor", "clinic", "prescriptions"):
    past_appointments_tree.column(col, anchor="center", width=100, stretch=ctk.YES)

upcoming_appointments_label = ctk.CTkLabel(history_frame, text="UPCOMING APPOINTMENTS", fg_color="lightblue", font=("Arial", 18))
upcoming_appointments_label.pack(fill=ctk.X, pady=(10, 0))

upcoming_appointments_tree = ttk.Treeview(history_frame, columns=("date", "time", "reason", "doctor", "clinic"), show='headings')
upcoming_appointments_tree.heading("date", text="Date")
upcoming_appointments_tree.heading("time", text="Time")
upcoming_appointments_tree.heading("reason", text="Reason")
upcoming_appointments_tree.heading("doctor", text="Doctor")
upcoming_appointments_tree.heading("clinic", text="Clinic")
upcoming_appointments_tree.pack(fill=ctk.BOTH, expand=True)

for col in ("date", "time", "reason", "doctor", "clinic"):
    upcoming_appointments_tree.column(col, anchor="center", width=100, stretch=ctk.YES)

# Fetch appointment data for the specific patient
past_appointments, upcoming_appointments = fetch_appointments(patient_id)

# Insert data into the tables
for appointment in past_appointments:
    past_appointments_tree.insert("", "end", values=appointment)

for appointment in upcoming_appointments:
    upcoming_appointments_tree.insert("", "end", values=appointment)

back_button = ctk.CTkButton(main_frame, text="Back", command=back_action, fg_color="#4BAAC8", text_color="white", font=("Arial", 12))
back_button.pack(pady=10)

root.mainloop()

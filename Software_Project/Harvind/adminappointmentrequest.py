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

# Function to go back to the clinic admin home page
def back_to_home():
    root.destroy()
    subprocess.run(['python', 'adminclinichome.py', clinic_id, admin_fullname])

# Create main window
root = tk.Tk()
root.title(f"Admin Appointment Requests - {clinic_id}")
root.geometry("1300x800")
root.configure(bg="white")

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

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

# Back button
back_btn = tk.Button(main_frame, text="Back", command=back_to_home, bg="blue", fg="white", font=("Arial", 12, "bold"))
back_btn.pack(pady=20)

# Initialize appointment requests in the table
refresh_appointment_requests()

root.mainloop()
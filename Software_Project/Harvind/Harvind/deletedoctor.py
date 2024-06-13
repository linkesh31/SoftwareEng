import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
import sys

# Get clinic ID from command line arguments
if len(sys.argv) > 1:
    clinic_id = sys.argv[1]
else:
    clinic_id = "Unknown Clinic"

# Function to delete a doctor
def delete_doctor(doctor_id, user_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute('DELETE FROM doctors WHERE doctor_id = %s', (doctor_id,))
        cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
        connection.commit()
        messagebox.showinfo("Success", "Doctor deleted successfully!")
        load_doctors()  # Refresh the table after deletion
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to load doctors from the database
def load_doctors():
    for widget in table_frame.winfo_children():
        widget.destroy()
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute('''
            SELECT doctors.doctor_id, users.user_id, users.fullname, users.email, users.phone_number, doctors.identification_number, doctors.gender 
            FROM doctors 
            JOIN users ON doctors.user_id = users.user_id 
            WHERE doctors.clinic_id = %s
        ''', (clinic_id,))
        doctors = cursor.fetchall()
        create_table_header()
        for index, doctor in enumerate(doctors):
            create_table_row(index, doctor)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def confirm_delete(doctor_id, user_id):
    response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?")
    if response:
        delete_doctor(doctor_id, user_id)

def back_action():
    root.destroy()
    os.system(f'python clinicadminhome.py {clinic_id}')

def create_table_header():
    headers = ["Doctor Name", "Email", "Tel", "IC", "Gender", "Delete Option"]
    for col, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Helvetica", 12, "bold"), bg="white", borderwidth=1, relief="solid", padx=10, pady=5)
        label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

def create_table_row(index, doctor):
    for col, value in enumerate(doctor[2:]):
        label = tk.Label(table_frame, text=value, font=("Helvetica", 12), bg="white", borderwidth=1, relief="solid", padx=10, pady=5)
        label.grid(row=index + 1, column=col, sticky="nsew", padx=1, pady=1)
    delete_button = tk.Button(table_frame, text="Delete", command=lambda d=doctor[0], u=doctor[1]: confirm_delete(d, u), bg="red", fg="white", font=("Helvetica", 12))
    delete_button.grid(row=index + 1, column=len(doctor[2:]), sticky="nsew", padx=1, pady=1)

# Create main window
root = tk.Tk()
root.title("Delete Doctor")
root.geometry("1000x600")  # Adjusted window size for better visibility
root.configure(bg="white")

# Title label
title_label = tk.Label(root, text="Delete Doctor", font=("Helvetica", 24, "bold"), bg="white")
title_label.pack(pady=10)

# Table frame
table_frame = tk.Frame(root, bg="white")
table_frame.pack(pady=10, padx=100, fill=tk.BOTH, expand=True)  # Centering the table with padx

# Create the initial header for the table
create_table_header()

# Load doctors into the table
load_doctors()

# Back button
back_button = tk.Button(root, text="Back", command=back_action, bg="white", font=("Helvetica", 12))
back_button.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
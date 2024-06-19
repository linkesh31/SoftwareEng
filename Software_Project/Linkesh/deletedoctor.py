import customtkinter as ctk
import mysql.connector
import os
import sys

# Get clinic ID and admin full name from command line arguments
if len(sys.argv) > 2:
    clinic_id = sys.argv[1]
    admin_fullname = sys.argv[2]
else:
    clinic_id = "Unknown Clinic"
    admin_fullname = "ADMIN"

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
        ctk.CTkMessageBox.show_info("Success", "Doctor deleted successfully!")
        load_doctors()  # Refresh the table after deletion
    except mysql.connector.Error as err:
        ctk.CTkMessageBox.show_error("Database Error", f"Error: {err}")
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
        ctk.CTkMessageBox.show_error("Database Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def confirm_delete(doctor_id, user_id):
    response = ctk.CTkMessageBox.ask_yes_no("Confirm Delete", "Are you sure you want to delete this doctor?")
    if response == "yes":
        delete_doctor(doctor_id, user_id)

def back_action():
    root.destroy()
    os.system(f'python adminclinichome.py {clinic_id} {admin_fullname}')

def create_table_header():
    headers = ["Doctor Name", "Email", "Tel", "IC", "Gender", "Delete Option"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(table_frame, text=header, font=("Helvetica", 12, "bold"), pady=5, fg_color="#E0F7FA", text_color="black")
        label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        table_frame.grid_columnconfigure(col, weight=1)  # Make columns expandable

def create_table_row(index, doctor):
    for col, value in enumerate(doctor[2:]):
        label = ctk.CTkLabel(table_frame, text=value, font=("Helvetica", 12), pady=5, fg_color="#E0F7FA", text_color="black")
        label.grid(row=index + 1, column=col, sticky="nsew", padx=1, pady=1)
    delete_button = ctk.CTkButton(table_frame, text="Delete", command=lambda d=doctor[0], u=doctor[1]: confirm_delete(d, u), fg_color="red", text_color="white", font=("Helvetica", 12))
    delete_button.grid(row=index + 1, column=len(doctor[2:]), sticky="nsew", padx=1, pady=1)

# Create main window
root = ctk.CTk()
root.title("Delete Doctor")
root.geometry("1000x600")  # Adjusted window size for better visibility
root.configure(fg_color="lightblue")  # Change the background color of the main window

# Title label
title_label = ctk.CTkLabel(root, text="Delete Doctor", font=("Helvetica", 24, "bold"), fg_color="lightblue", text_color="black")
title_label.pack(pady=10)

# Table frame
table_frame = ctk.CTkFrame(root, fg_color="lightblue")
table_frame.pack(pady=10, padx=100, fill=ctk.BOTH, expand=True)  # Centering the table with padx

# Create the initial header for the table
create_table_header()

# Load doctors into the table
load_doctors()

# Back button
back_button = ctk.CTkButton(root, text="Back", command=back_action, font=("Helvetica", 12), text_color="Black", fg_color="#81D4FA")
back_button.pack(side=ctk.BOTTOM, pady=20)

root.mainloop()
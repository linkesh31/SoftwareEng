import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import sys
import os

# Fetch patient details based on patient_id
def fetch_patient_details(patient_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute('''
            SELECT u.fullname, u.username, p.identification_number, p.gender, u.address, u.date_of_birth, u.email, u.phone_number 
            FROM users u
            JOIN patients p ON u.user_id = p.user_id
            WHERE p.patient_id = %s
        ''', (patient_id,))
        result = cursor.fetchone()
        return result
    except Error as e:
        messagebox.showerror("Error", f"Error fetching patient details: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None

def back_to_home(patient_id, patient_fullname):
    root.destroy()
    os.system(f'python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/patienthome.py" {patient_id} {patient_fullname}')

def create_patient_profile_window(patient_id, patient_fullname):
    global root
    root = tk.Tk()
    root.title("Patient Profile")
    root.geometry("1000x700")  # Increased window size
    root.configure(bg="white")

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Fetch patient details
    patient_details = fetch_patient_details(patient_id)

    if not patient_details:
        messagebox.showerror("Error", "User details not found!")
        root.destroy()
        return

    # Profile section
    profile_frame = tk.Frame(main_frame, bg="#ff6b6b", padx=10, pady=10)
    profile_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    profile_label = tk.Label(profile_frame, text="PATIENT PROFILE", bg="#ff6b6b", font=("Arial", 16, "bold"))
    profile_label.grid(row=0, columnspan=2, pady=10)

    labels = ["Fullname:", "Username:", "IC:", "Gender:", "Address:", "Date of Birth:", "Email:", "Tel:"]
    
    for i, label_text in enumerate(labels):
        row = i % 4 + 1
        col = i // 4 * 2
        label = tk.Label(profile_frame, text=label_text, bg="#ff6b6b", font=("Arial", 12))
        label.grid(row=row, column=col, sticky="e", padx=5, pady=5)
        entry = tk.Entry(profile_frame, bg="white", font=("Arial", 12))
        entry.grid(row=row, column=col + 1, sticky="w", padx=5, pady=5)
        entry.insert(0, patient_details[i])
        entry.config(state='readonly')

    edit_button = tk.Button(profile_frame, text="Edit Profile", font=("Arial", 12), bg="white", command=lambda: edit_profile_action(root, patient_id, patient_fullname))
    edit_button.grid(row=5, columnspan=4, pady=10)

    back_button = tk.Button(profile_frame, text="Back", font=("Arial", 12), bg="white", command=lambda: back_to_home(patient_id, patient_fullname))
    back_button.grid(row=6, columnspan=4, pady=10)

    root.mainloop()

def edit_profile_action(root, patient_id, patient_fullname):
    root.destroy()
    import patienteditprofile
    patienteditprofile.create_patient_edit_profile_window(patient_id, patient_fullname)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        patient_id = int(sys.argv[1])
        patient_fullname = sys.argv[2]
    else:
        patient_id = 1  # Default patient_id for testing
        patient_fullname = "PATIENT"

    create_patient_profile_window(patient_id, patient_fullname)
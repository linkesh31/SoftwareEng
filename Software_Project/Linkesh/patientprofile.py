import customtkinter as ctk
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
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/patienthome.py" {patient_id} {patient_fullname}')

def create_patient_profile_window(patient_id, patient_fullname):
    global root
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = ctk.CTk()
    root.title("Patient Profile")
    root.geometry("550x550")  # Increased window size

    # Main content area
    main_frame = ctk.CTkFrame(root, fg_color="lightblue")
    main_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)

    # Fetch patient details
    patient_details = fetch_patient_details(patient_id)

    if not patient_details:
        messagebox.showerror("Error", "User details not found!")
        root.destroy()
        return

    # Profile section
    profile_frame = ctk.CTkFrame(main_frame, fg_color="lightblue", corner_radius=10)
    profile_frame.pack(expand=True, pady=10, ipadx=20, ipady=20)

    profile_label = ctk.CTkLabel(profile_frame, text="PATIENT PROFILE", font=("Arial", 16, "bold"))
    profile_label.grid(row=0, columnspan=2, pady=20)

    labels = ["Fullname:", "Username:", "IC:", "Gender:", "Address:", "Date of Birth:", "Email:", "Tel:"]
    
    for i, label_text in enumerate(labels):
        label = ctk.CTkLabel(profile_frame, text=label_text, font=("Arial", 12))
        label.grid(row=i + 1, column=0, sticky="e", padx=5, pady=5)
        entry = ctk.CTkEntry(profile_frame, font=("Arial", 12))
        entry.grid(row=i + 1, column=1, sticky="w", padx=5, pady=5)
        entry.insert(0, patient_details[i])
        entry.configure(state='readonly')

    edit_button = ctk.CTkButton(profile_frame, text="Edit Profile", font=("Arial", 12), command=lambda: edit_profile_action(root, patient_id, patient_fullname))
    edit_button.grid(row=len(labels) + 1, columnspan=2, pady=10)

    back_button = ctk.CTkButton(profile_frame, text="Back", font=("Arial", 12), command=lambda: back_to_home(patient_id, patient_fullname))
    back_button.grid(row=len(labels) + 2, columnspan=2, pady=10)

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

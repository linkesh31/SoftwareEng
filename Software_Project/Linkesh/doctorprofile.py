import sys
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import os


# Fetch doctor details based on doctor_id
def fetch_doctor_details(doctor_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute('''
            SELECT d.fullname, u.username, d.identification_number, d.gender, u.address, u.date_of_birth, u.email, u.phone_number 
            FROM users u
            JOIN doctors d ON u.user_id = d.user_id
            WHERE d.doctor_id = %s
        ''', (doctor_id,))
        result = cursor.fetchone()
        return result
    except Error as e:
        messagebox.showerror("Error", f"Error fetching doctor details: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None


def back_to_home(doctor_id):
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/doctorhome.py" {doctor_id}')


def create_doctor_profile_window(doctor_id):
    global root
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = ctk.CTk()
    root.title("Doctor Profile")
    root.geometry("550x550")  # Adjusted window size to match patient profile

    # Main content area
    main_frame = ctk.CTkFrame(root, fg_color="lightblue")
    main_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)

    # Fetch doctor details
    doctor_details = fetch_doctor_details(doctor_id)

    if not doctor_details:
        messagebox.showerror("Error", "Doctor details not found!")
        root.destroy()
        return

    # Profile section
    profile_frame = ctk.CTkFrame(main_frame, fg_color="lightblue", corner_radius=10)
    profile_frame.pack(expand=True, pady=10, ipadx=20, ipady=20)

    profile_label = ctk.CTkLabel(profile_frame, text="DOCTOR PROFILE", font=("Arial", 16, "bold"))
    profile_label.grid(row=0, columnspan=2, pady=20)

    labels = ["Fullname:", "Username:", "IC:", "Gender:", "Address:", "Date of Birth:", "Email:", "Tel:"]

    for i, label_text in enumerate(labels):
        label = ctk.CTkLabel(profile_frame, text=label_text, font=("Arial", 12))
        label.grid(row=i + 1, column=0, sticky="e", padx=5, pady=5)
        entry = ctk.CTkEntry(profile_frame, font=("Arial", 12))
        entry.grid(row=i + 1, column=1, sticky="w", padx=5, pady=5)
        entry.insert(0, doctor_details[i])
        entry.configure(state='readonly')

    edit_button = ctk.CTkButton(profile_frame, text="Edit Profile", font=("Arial", 12),
                                command=lambda: edit_profile_action(root, doctor_id))
    edit_button.grid(row=len(labels) + 1, columnspan=2, pady=10)

    back_button = ctk.CTkButton(profile_frame, text="Back", font=("Arial", 12),
                                command=lambda: back_to_home(doctor_id))
    back_button.grid(row=len(labels) + 2, columnspan=2, pady=10)

    root.mainloop()


def edit_profile_action(root, doctor_id):
    root.destroy()
    import doctoreditprofile
    doctoreditprofile.create_doctor_edit_profile_window(doctor_id)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        doctor_id = int(sys.argv[1])
    else:
        doctor_id = 1  # Example doctor_id for testing

    create_doctor_profile_window(doctor_id)

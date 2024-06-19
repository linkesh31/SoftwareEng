import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import patientprofile
import os
import sys

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

def update_patient_details(patient_id, address, email, phone_number):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE users u
            JOIN patients p ON u.user_id = p.user_id
            SET u.address = %s, u.email = %s, u.phone_number = %s
            WHERE p.patient_id = %s
        ''', (address, email, phone_number, patient_id))
        connection.commit()
    except Error as e:
        messagebox.showerror("Error", f"Error updating patient details: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def load_image(image_path, size):
    try:
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading image {image_path}: {e}")
        return None

def back_to_home(root, patient_id, patient_fullname):
    root.destroy()
    patientprofile.create_patient_profile_window(patient_id, patient_fullname)

def validate_phone_number(phone_number):
    if not phone_number.isdigit():
        messagebox.showerror("Invalid Input", "Phone number must contain only digits.")
        return False
    return True

def create_patient_edit_profile_window(patient_id, patient_fullname):
    global root
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = ctk.CTk()
    root.title("Edit Profile (You can only edit the blue field)")
    root.geometry("550x550")  # Match the window size with patientprofile

    # Main content area
    main_frame = ctk.CTkFrame(root, fg_color="lightblue")
    main_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)

    # Profile section
    profile_frame = ctk.CTkFrame(main_frame, fg_color="lightblue", corner_radius=10)
    profile_frame.pack(expand=True, pady=10, ipadx=20, ipady=20)

    profile_label = ctk.CTkLabel(profile_frame, text="EDIT PROFILE (You can only edit the white field)", font=("Arial", 16, "bold"))
    profile_label.grid(row=0, columnspan=2, pady=20)

    labels = ["Fullname:", "Username:", "IC:", "Gender:", "Address:", "Date of Birth:", "Email:", "Tel:"]
    patient_details = fetch_patient_details(patient_id)
    entries = []

    if patient_details:
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(profile_frame, text=label_text, font=("Arial", 12))
            label.grid(row=i + 1, column=0, sticky="e", padx=5, pady=5)
            entry_fg_color = "white" if label_text in ["Address:", "Email:", "Tel:"] else "lightblue"
            entry = ctk.CTkEntry(profile_frame, font=("Arial", 12), fg_color=entry_fg_color)
            entry.grid(row=i + 1, column=1, sticky="w", padx=5, pady=5)
            entry.insert(0, patient_details[i])
            if label_text not in ["Address:", "Email:", "Tel:"]:
                entry.configure(state='readonly')
            entries.append(entry)

        def save_changes():
            address = entries[4].get()
            email = entries[6].get()
            phone_number = entries[7].get()
            if not validate_phone_number(phone_number):
                return
            update_patient_details(patient_id, address, email, phone_number)
            messagebox.showinfo("Success", "Profile updated successfully")
            root.destroy()
            patientprofile.create_patient_profile_window(patient_id, patient_fullname)

        def confirm_changes():
            response = messagebox.askyesno("Confirm Changes", "Are you sure you want to make the changes?")
            if response:
                save_changes()

        confirm_button = ctk.CTkButton(profile_frame, text="Confirm", font=("Arial", 12), command=confirm_changes)
        confirm_button.grid(row=len(labels) + 1, columnspan=2, pady=10)

        back_button = ctk.CTkButton(profile_frame, text="Back", font=("Arial", 12), command=lambda: back_to_home(root, patient_id, patient_fullname))
        back_button.grid(row=len(labels) + 2, columnspan=2, pady=10)
    else:
        messagebox.showerror("Error", "User details not found!")

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        patient_id = int(sys.argv[1])
        patient_fullname = sys.argv[2]
    else:
        patient_id = 1  # Default patient_id for testing
        patient_fullname = "PATIENT"

    create_patient_edit_profile_window(patient_id, patient_fullname)

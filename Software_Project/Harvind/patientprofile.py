import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import patienthome  # Import the patienthome module
import os

def fetch_patient_details(username):
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
            WHERE u.username = %s
        ''', (username,))
        result = cursor.fetchone()
        return result
    except Error as e:
        messagebox.showerror("Error", f"Error fetching patient details: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None

def back_to_home(username):
    root.destroy()
    patienthome.create_patient_home_window(username)  # Navigate back to patient home

def create_patient_profile_window(username):
    global root
    root = tk.Tk()
    root.title("Patient Profile")
    root.geometry("1000x700")  # Increased window size
    root.configure(bg="white")

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Fetch patient details
    patient_details = fetch_patient_details(username)

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

    edit_button = tk.Button(profile_frame, text="Edit Profile", font=("Arial", 12), bg="white", command=lambda: edit_profile_action(root, username))
    edit_button.grid(row=5, columnspan=4, pady=10)

    back_button = tk.Button(profile_frame, text="Back", font=("Arial", 12), bg="white", command=lambda: back_to_home(username))
    back_button.grid(row=6, columnspan=4, pady=10)

    root.mainloop()

def edit_profile_action(root, username):
    root.destroy()
    import patienteditprofile
    patienteditprofile.create_patient_edit_profile_window(username)

if __name__ == "__main__":
    create_patient_profile_window("")

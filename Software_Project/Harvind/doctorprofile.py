import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
import subprocess

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

def load_image(image_path, size):
    try:
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading image {image_path}: {e}")
        return None

def back_to_home(doctor_id):
    root.destroy()
    subprocess.run(['python', 'doctorhome.py', str(doctor_id)])

def create_doctor_profile_window(doctor_id):
    global root
    root = tk.Tk()
    root.title("Doctor Profile")
    root.geometry("1000x700")  # Increased window size
    root.configure(bg="white")

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Fetch doctor details
    doctor_details = fetch_doctor_details(doctor_id)

    if not doctor_details:
        messagebox.showerror("Error", "Doctor details not found!")
        root.destroy()
        return

    # Profile section
    profile_frame = tk.Frame(main_frame, bg="#ff6b6b", padx=10, pady=10)
    profile_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    profile_label = tk.Label(profile_frame, text="DOCTOR PROFILE", bg="#ff6b6b", font=("Arial", 16, "bold"))
    profile_label.grid(row=0, columnspan=2, pady=10)

    labels = ["Fullname:", "Username:", "Identification Number:", "Gender:", "Address:", "Date of Birth:", "Email:", "Tel:"]
    
    for i, label_text in enumerate(labels):
        row = i % 4 + 1
        col = i // 4 * 2
        label = tk.Label(profile_frame, text=label_text, bg="#ff6b6b", font=("Arial", 12))
        label.grid(row=row, column=col, sticky="e", padx=5, pady=5)
        entry = tk.Entry(profile_frame, bg="white" if label_text in ["Address:", "Email:", "Tel:"] else "#EC7063", font=("Arial", 12))
        entry.grid(row=row, column=col + 1, sticky="w", padx=5, pady=5)
        entry.insert(0, doctor_details[i])
        entry.config(state='readonly')

    edit_button = tk.Button(profile_frame, text="Edit Profile", font=("Arial", 12), bg="white", command=lambda: edit_profile_action(root, doctor_id))
    edit_button.grid(row=5, columnspan=4, pady=10)

    back_button = tk.Button(profile_frame, text="Back", font=("Arial", 12), bg="white", command=lambda: back_to_home(doctor_id))
    back_button.grid(row=6, columnspan=4, pady=10)

    root.mainloop()

def edit_profile_action(root, doctor_id):
    root.destroy()
    import doctoreditprofile
    doctoreditprofile.create_doctor_edit_profile_window(doctor_id)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        doctor_id = int(sys.argv[1])
    else:
        doctor_id = 15  # Example doctor_id for testing

    create_doctor_profile_window(doctor_id)
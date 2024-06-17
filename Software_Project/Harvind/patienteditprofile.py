import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import patientprofile
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

def update_patient_details(username, address, email, phone_number):
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
            WHERE u.username = %s
        ''', (address, email, phone_number, username))
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

def back_to_home(root, username):
    root.destroy()
    patientprofile.create_patient_profile_window(username)

def create_patient_edit_profile_window(username):
    global root
    root = tk.Tk()
    root.title("Edit Profile")
    root.geometry("1000x700")  # Increased window size
    root.configure(bg="white")

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Profile section
    profile_frame = tk.Frame(main_frame, bg="#ff6b6b", padx=10, pady=10)
    profile_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    profile_label = tk.Label(profile_frame, text="EDIT PROFILE", bg="#ff6b6b", font=("Arial", 16, "bold"))
    profile_label.grid(row=0, columnspan=2, pady=10)

    labels = ["Fullname:", "Username:", "IC:", "Gender:", "Address:", "Date of Birth:", "Email:", "Tel:"]
    patient_details = fetch_patient_details(username)
    entries = []

    if patient_details:
        for i, label_text in enumerate(labels):
            row = i % 4 + 1
            col = i // 4 * 2
            label = tk.Label(profile_frame, text=label_text, bg="#ff6b6b", font=("Arial", 12))
            label.grid(row=row, column=col, sticky="e", padx=5, pady=5)
            entry = tk.Entry(profile_frame, bg="lightblue" if label_text in ["Address:", "Email:", "Tel:"] else "#f0f0f0", font=("Arial", 12))
            entry.grid(row=row, column=col + 1, sticky="w", padx=5, pady=5)
            entry.insert(0, patient_details[i])
            if label_text not in ["Address:", "Email:", "Tel:"]:
                entry.config(state='readonly')
            entries.append(entry)

        def save_changes():
            address = entries[4].get()
            email = entries[6].get()
            phone_number = entries[7].get()
            update_patient_details(username, address, email, phone_number)
            messagebox.showinfo("Success", "Profile updated successfully")
            root.destroy()
            patientprofile.create_patient_profile_window(username)

        def confirm_changes():
            response = messagebox.askyesno("Confirm Changes", "Are you sure you want to make the changes?")
            if response:
                save_changes()

        back_button = tk.Button(profile_frame, text="Back", font=("Arial", 12), bg="white", command=lambda: back_to_home(root, username))
        back_button.grid(row=5, column=0, pady=10)

        confirm_button = tk.Button(profile_frame, text="Confirm", font=("Arial", 12), bg="white", command=confirm_changes)
        confirm_button.grid(row=5, column=1, pady=10)
    else:
        messagebox.showerror("Error", "User details not found!")

    root.mainloop()

if __name__ == "__main__":
    create_patient_edit_profile_window("")
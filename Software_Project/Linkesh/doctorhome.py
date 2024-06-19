import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import os
import sys
import subprocess

# Function to fetch doctor's full name
def get_doctor_fullname(doctor_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="calladoctor1234",
            database="calladoctor"
        )
        cursor = db.cursor()
        cursor.execute("SELECT fullname FROM doctors WHERE doctor_id = %s", (doctor_id,))
        result = cursor.fetchone()
        db.close()
        if result:
            return result[0]
        else:
            raise ValueError(f"No doctor found with ID {doctor_id}")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        return "Doctor"

# Function to fetch appointments
def fetch_appointments(doctor_id):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="calladoctor1234",
            database="calladoctor"
        )
        cursor = connection.cursor()

        # Fetch past appointments
        cursor.execute("""
            SELECT a.appointment_date, a.appointment_time, p.fullname, a.reason, IFNULL(pr.medical_report, 'N/A')
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            LEFT JOIN prescriptions pr ON a.appointment_id = pr.appointment_id
            WHERE a.doctor_id = %s AND a.treatment_status = 'done'
            ORDER BY a.appointment_date DESC
        """, (doctor_id,))
        past_appointments = cursor.fetchall()

        # Fetch upcoming appointments
        cursor.execute("""
            SELECT a.appointment_id, a.appointment_date, a.appointment_time, p.fullname, a.reason
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = %s AND a.treatment_status = 'pending' AND a.appointment_request_status = 'accepted'
            ORDER BY a.appointment_date ASC
        """, (doctor_id,))
        upcoming_appointments = cursor.fetchall()

        cursor.close()
        connection.close()

        return past_appointments, upcoming_appointments
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
        return [], []

# Function to create prescription form and save the prescription
def create_prescription_form(appointment_id, doctor_id, patient_name):
    def save_prescription():
        prescription = text.get("1.0", ctk.END).strip()
        if prescription:
            response = messagebox.askyesno("Confirmation",
                                           "This will result in completing the patient's appointment. Do you want to proceed?")
            if response:
                try:
                    connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="calladoctor1234",
                        database="calladoctor"
                    )
                    cursor = connection.cursor()
                    cursor.execute("""
                        INSERT INTO prescriptions (appointment_id, doctor_id, patient_id, medical_report)
                        VALUES (%s, %s, (SELECT patient_id FROM appointments WHERE appointment_id = %s), %s)
                    """, (appointment_id, doctor_id, appointment_id, prescription))
                    cursor.execute("""
                        UPDATE appointments
                        SET treatment_status = 'done'
                        WHERE appointment_id = %s
                    """, (appointment_id,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    refresh_appointments()
                    messagebox.showinfo("Success", "Prescription saved successfully.")
                    prescription_window.destroy()
                    root.deiconify()  # Re-enable the main window
                except mysql.connector.Error as err:
                    print(f"Database Error: {err}")
                    messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Warning", "Prescription cannot be empty.")

    def go_back():
        prescription_window.destroy()
        root.deiconify()  # Re-enable the main window

    root.withdraw()  # Disable the main window

    prescription_window = ctk.CTkToplevel(root)
    prescription_window.title("Prescription")
    prescription_window.geometry("400x300")

    label = ctk.CTkLabel(prescription_window, text=f"Enter Prescription for {patient_name}:")
    label.pack(pady=10)
    text = ctk.CTkTextbox(prescription_window, height=10, width=40)
    text.pack(pady=10)

    button_frame = ctk.CTkFrame(prescription_window)
    button_frame.pack(pady=10)

    save_button = ctk.CTkButton(button_frame, text="Save", command=save_prescription)
    save_button.pack(side=ctk.LEFT, padx=5)

    back_button = ctk.CTkButton(button_frame, text="Back", command=go_back)
    back_button.pack(side=ctk.LEFT, padx=5)

# Function for button actions
def profile_action():
    root.destroy()
    subprocess.run(['python', 'doctorprofile.py', str(doctor_id)])

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

# Function to refresh the appointments table
def refresh_appointments():
    past_appointments, upcoming_appointments = fetch_appointments(doctor_id)

    for widget in past_appointments_frame.winfo_children():
        widget.destroy()
    for widget in upcoming_appointments_frame.winfo_children():
        widget.destroy()

    past_columns = ["Date", "Time", "Patient Name", "Reason", "Prescription"]
    for col in past_columns:
        header = ctk.CTkLabel(past_appointments_frame, text=col, font=("Arial", 10, "bold"), fg_color="#E0F7FA", padx=5,
                              pady=5)
        header.grid(row=0, column=past_columns.index(col), sticky="nsew")

    for i, appointment in enumerate(past_appointments):
        for j, value in enumerate(appointment):
            label = ctk.CTkLabel(past_appointments_frame, text=value, font=("Arial", 10), fg_color="white", padx=5,
                                 pady=5)
            label.grid(row=i + 1, column=j, sticky="nsew")

    for col in range(len(past_columns)):
        past_appointments_frame.grid_columnconfigure(col, weight=1)

    upcoming_columns = ["Date", "Time", "Patient Name", "Reason", "Action (Click to generate prescription)"]
    for col in upcoming_columns:
        header = ctk.CTkLabel(upcoming_appointments_frame, text=col, font=("Arial", 10, "bold"), fg_color="#E0F7FA",
                              padx=5, pady=5)
        header.grid(row=0, column=upcoming_columns.index(col), sticky="nsew")

    for i, appointment in enumerate(upcoming_appointments):
        appointment_id, date, time, patient_name, reason = appointment
        for j, value in enumerate(appointment[1:]):
            label = ctk.CTkLabel(upcoming_appointments_frame, text=value, font=("Arial", 10), fg_color="white", padx=5,
                                 pady=5)
            label.grid(row=i + 1, column=j, sticky="nsew")
        prescribe_button = ctk.CTkButton(upcoming_appointments_frame, text="Not prescribed",
                                         command=lambda appt_id=appointment_id,
                                                        pt_name=patient_name: create_prescription_form(appt_id,
                                                                                                       doctor_id,
                                                                                                       pt_name),
                                         fg_color="blue", text_color="white", font=("Arial", 10))
        prescribe_button.grid(row=i + 1, column=len(appointment[1:]), sticky="nsew")

    for col in range(len(upcoming_columns)):
        upcoming_appointments_frame.grid_columnconfigure(col, weight=1)

# Get doctor_id from command-line arguments
doctor_id = sys.argv[1] if len(sys.argv) > 1 else None
if doctor_id:
    try:
        doctor_id = int(doctor_id)
        doctor_fullname = get_doctor_fullname(doctor_id)
    except ValueError as ve:
        print(f"ValueError: {ve}")
        doctor_fullname = "Unknown Doctor"
else:
    doctor_fullname = "Unknown Doctor"

# Create main window
ctk.set_appearance_mode("light")  # Modes: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Doctor Home Page")
root.geometry("1000x700")  # Adjusted window size
root.configure(fg_color="#AED6F1")  # Set the main window background color

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=img, size=size)

# Load images with specified size
button_size = (40, 40)
profile_img = load_image("profile.png", button_size)
logout_img = load_image("logout.png", button_size)

# Left side menu
menu_frame = ctk.CTkFrame(root, fg_color="#E6E6FA")
menu_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)

# Menu buttons with images and labels
def create_button(frame, image, text, command):
    button_frame = ctk.CTkFrame(frame, fg_color="#E6E6FA")
    button_frame.pack(fill=ctk.X, pady=5, padx=5)
    btn = ctk.CTkButton(button_frame, image=image, command=command, fg_color="white", hover_color="#AED6F1", text="")
    btn.pack(pady=0)
    label = ctk.CTkLabel(button_frame, text=text, fg_color="#E6E6FA", font=("Arial", 12, "bold"))
    label.pack(pady=5)
    return button_frame

create_button(menu_frame, profile_img, "PROFILE", profile_action)
create_button(menu_frame, logout_img, "LOGOUT", logout_action)

# Main content area
main_frame = ctk.CTkFrame(root, fg_color="#AED6F1")
main_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

# Welcome text
welcome_label = ctk.CTkLabel(main_frame, text=f"Welcome DR. {doctor_fullname}", font=("Arial", 24), fg_color="#AED6F1")
welcome_label.pack(pady=20)

# Past appointments section
past_appointments_label = ctk.CTkLabel(main_frame, text="PAST APPOINTMENTS", fg_color="#AED6F1", font=("Arial", 14))
past_appointments_label.pack(fill=ctk.X, pady=(0, 10))

past_appointments_frame = ctk.CTkFrame(main_frame, fg_color="white")
past_appointments_frame.pack(fill=ctk.BOTH, expand=True)

# Upcoming appointments section
upcoming_appointments_label = ctk.CTkLabel(main_frame, text="UPCOMING APPOINTMENTS", fg_color="#AED6F1",
                                           font=("Arial", 14))
upcoming_appointments_label.pack(fill=ctk.X, pady=(10, 0))

upcoming_appointments_frame = ctk.CTkFrame(main_frame, fg_color="white")
upcoming_appointments_frame.pack(fill=ctk.BOTH, expand=True)

# Fetch appointment data for the specific doctor
refresh_appointments()

root.mainloop()
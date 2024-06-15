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

def load_image(image_path, size):
    try:
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading image {image_path}: {e}")
        return None

def create_buttons(menu_frame, image_path, username):
    button_size = (40, 40)
    buttons_info = [
        ("home.jpg", "HOME", lambda: back_to_home(root, username)),
        ("search.jpg", "SEARCH/VIEW CLINIC", search_view_clinic_action),
        ("sendrequest.jpg", "SEND REQUEST TO DOCTOR", send_request_to_doctor_action),
        ("profile.jpg", "PROFILE", lambda: profile_action(username)),
        ("appointment.jpg", "APPOINTMENT SUMMARY", appointment_summary_action),
        ("logout.jpg", "LOGOUT", logout_action)
    ]
    for image_name, text, command in buttons_info:
        image = load_image(image_path + image_name, button_size)
        if image:
            create_button(menu_frame, image, text, command)

def create_button(frame, image, text, command):
    btn = tk.Button(frame, image=image, command=command, bg="white", compound=tk.TOP)
    btn.pack(pady=5)
    btn.image = image  # Keep a reference to avoid garbage collection
    label = tk.Label(frame, text=text, bg="white", font=("Arial", 10))
    label.pack()

def search_view_clinic_action():
    messagebox.showinfo("Search/View Clinic", "Search/View Clinic Button Clicked")

def send_request_to_doctor_action():
    messagebox.showinfo("Send Request to Doctor", "Send Request to Doctor Button Clicked")

def profile_action(username):
    messagebox.showinfo("Profile", "Already on the profile page")

def appointment_summary_action():
    messagebox.showinfo("Appointment Summary", "Appointment Summary Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def back_to_home(root, username):
    root.destroy()
    patienthome.create_patient_home_window(username)  # Navigate back to patient home

def create_patient_profile_window(username):
    global root
    root = tk.Tk()
    root.title("Patient Profile")
    root.geometry("1000x700")  # Increased window size
    root.configure(bg="white")

    image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

    # Left side menu
    menu_frame = tk.Frame(root, bg="white")
    menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Load images and create buttons
    create_buttons(menu_frame, image_path, username)

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Fetch patient details
    patient_details = fetch_patient_details(username)

    if not patient_details:
        messagebox.showerror("Error", "User details not found!")
        root.destroy()
        return

    fullname = patient_details[0]  # Full name is the first item in patient_details

    # Welcome text
    welcome_label = tk.Label(main_frame, text=f"Welcome {fullname}", font=("Arial", 24), bg="white")
    welcome_label.pack(pady=20)

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

    root.mainloop()

def edit_profile_action(root, username):
    root.destroy()
    import patienteditprofile
    patienteditprofile.create_patient_edit_profile_window(username)

if __name__ == "__main__":
    create_patient_profile_window("patient1")
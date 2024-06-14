import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
import patientprofile  # Import the patientprofile module

def fetch_fullname(username, label):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute('''
            SELECT fullname FROM users WHERE username = %s
        ''', (username,))
        result = cursor.fetchone()
        if result:
            fullname = result[0]
            label.config(text=f"Welcome {fullname}")
        else:
            messagebox.showerror("Error", "User not found!")
    except Error as e:
        messagebox.showerror("Error", f"Error fetching full name: {e}")
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

def create_buttons(menu_frame, image_path, username):
    button_size = (40, 40)
    buttons_info = [
        ("home.png", "HOME", home_action),
        ("search.png", "SEARCH/VIEW CLINIC", search_view_clinic_action),
        ("sendrequest.png", "SEND REQUEST TO DOCTOR", send_request_to_doctor_action),
        ("profile.png", "PROFILE", lambda: profile_action(username)),
        ("appointment.png", "APPOINTMENT SUMMARY", appointment_summary_action),
        ("logout.png", "LOGOUT", logout_action)
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

def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def search_view_clinic_action():
    messagebox.showinfo("Search/View Clinic", "Search/View Clinic Button Clicked")

def send_request_to_doctor_action():
    messagebox.showinfo("Send Request to Doctor", "Send Request to Doctor Button Clicked")

def profile_action(username):
    root.destroy()
    patientprofile.create_patient_profile_window(username)

def appointment_summary_action():
    messagebox.showinfo("Appointment Summary", "Appointment Summary Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

def create_patient_home_window(username):
    global root
    root = tk.Tk()
    root.title("Appointment System")
    root.geometry("800x600")
    root.configure(bg="white")

    image_path = "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/Images/"

    # Left side menu
    menu_frame = tk.Frame(root, bg="white")
    menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Welcome text
    welcome_label = tk.Label(main_frame, text="Welcome", font=("Arial", 24), bg="white")
    welcome_label.pack(pady=20)

    # Fetch user's full name from the database
    fetch_fullname(username, welcome_label)

    # Load images and create buttons
    create_buttons(menu_frame, image_path, username)

    # Appointment history section
    history_frame = tk.Frame(main_frame, bg="lightblue", padx=10, pady=10)
    history_frame.pack(fill=tk.BOTH, expand=True)

    past_appointments_label = tk.Label(history_frame, text="PAST APPOINTMENTS", bg="lightblue", font=("Arial", 14))
    past_appointments_label.pack(fill=tk.X, pady=(0, 10))

    # Past appointments list (placeholder)
    past_appointments_list = tk.Listbox(history_frame)
    past_appointments_list.pack(fill=tk.BOTH, expand=True)

    upcoming_appointments_label = tk.Label(history_frame, text="UPCOMING APPOINTMENTS", bg="lightblue", font=("Arial", 14))
    upcoming_appointments_label.pack(fill=tk.X, pady=(10, 0))

    # Upcoming appointments list (placeholder)
    upcoming_appointments_list = tk.Listbox(history_frame)
    upcoming_appointments_list.pack(fill=tk.BOTH, expand=True)

    # Notification button with image
    notification_img = load_image(image_path + "bell.png", (30, 30))
    if notification_img:
        notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
        notification_btn.image = notification_img  # Keep a reference to avoid garbage collection
        notification_btn.place(x=760, y=20)

    root.mainloop()

if __name__ == "__main__":
    create_patient_home_window("patient1")

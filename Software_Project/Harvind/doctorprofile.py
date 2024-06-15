import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os

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

def create_buttons(menu_frame, image_path, doctor_id):
    button_size = (40, 40)
    buttons_info = [
        ("home.png", "HOME", lambda: back_to_home(root, doctor_id)),
        ("listofpatients.png", "LIST OF PATIENTS", list_of_patients_action),
        ("profile.png", "PROFILE", lambda: profile_action(doctor_id)),
        ("availability.png", "AVAILABILITY STATUS", availability_status_action),
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

def list_of_patients_action():
    messagebox.showinfo("List of Patients", "List of Patients Button Clicked")

def profile_action(doctor_id):
    messagebox.showinfo("Profile", "Already on the profile page")

def availability_status_action():
    messagebox.showinfo("Availability Status", "Availability Status Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/main_page.py"')

def back_to_home(root, doctor_id):
    root.destroy()
    import doctorhome
    doctorhome.create_doctor_home_window(doctor_id)

def create_doctor_profile_window(doctor_id):
    global root
    root = tk.Tk()
    root.title("Doctor Profile")
    root.geometry("1000x700")  # Increased window size
    root.configure(bg="white")

    image_path = "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/Images/"

    # Left side menu
    menu_frame = tk.Frame(root, bg="white")
    menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Load images and create buttons
    create_buttons(menu_frame, image_path, doctor_id)

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Fetch doctor details
    doctor_details = fetch_doctor_details(doctor_id)

    if not doctor_details:
        messagebox.showerror("Error", "Doctor details not found!")
        root.destroy()
        return

    fullname = doctor_details[0]  # Full name is the first item in doctor_details

    # Welcome text
    welcome_label = tk.Label(main_frame, text=f"Welcome Dr. {fullname}", font=("Arial", 24), bg="white")
    welcome_label.pack(pady=20)

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

    root.mainloop()

def edit_profile_action(root, doctor_id):
    root.destroy()
    import doctoreditprofile
    doctoreditprofile.create_doctor_edit_profile_window(doctor_id)

if __name__ == "__main__":
    create_doctor_profile_window(15)  # Example doctor_id for testing

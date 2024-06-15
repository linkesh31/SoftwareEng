import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess

# Database connection function to fetch patient data
def fetch_patients():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="calladoctor1234",
            database="calladoctor"
        )
        cursor = db.cursor()
        cursor.execute("SELECT date, time, name, reason, prescriptions FROM patients")
        result = cursor.fetchall()
        db.close()
        return result
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# Button action functions
def home_action():
    messagebox.showinfo("Home", "Home Button Clicked")

def list_of_patients_action():
    pass  # Already on the list of patients page

def profile_action():
    messagebox.showinfo("Profile", "Profile Button Clicked")

def availability_status_action():
    messagebox.showinfo("Availability Status", "Availability Status Button Clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        subprocess.run(['python', 'main_page.py'])

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

# Create the patient list window
def create_patient_list_window():
    global root
    root = tk.Tk()
    root.title("List of Patients")
    root.geometry("800x600")
    root.configure(bg="white")

    # Image file path
    image_path = "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/Images/"

    # Function to load and resize images
    def load_image(image_name, size):
        img = Image.open(image_path + image_name)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    # Load images with specified size
    button_size = (40, 40)
    home_img = load_image("home.png", button_size)
    list_of_patients_img = load_image("listofpatients.png", button_size)
    profile_img = load_image("profile.png", button_size)
    availability_status_img = load_image("availability.png", button_size)
    logout_img = load_image("logout.png", button_size)
    notification_img = load_image("bell.png", (30, 30))  # Load and resize the notification bell icon

    # Left side menu
    menu_frame = tk.Frame(root, bg="white")
    menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Menu buttons with images and labels
    def create_button(frame, image, text, command):
        btn = tk.Button(frame, image=image, command=command, bg="white", compound=tk.TOP)
        btn.pack(pady=5)
        label = tk.Label(frame, text=text, bg="white", font=("Arial", 10))
        label.pack()

    create_button(menu_frame, home_img, "HOME", home_action)
    create_button(menu_frame, list_of_patients_img, "LIST OF PATIENTS", list_of_patients_action)
    create_button(menu_frame, profile_img, "PROFILE", profile_action)
    create_button(menu_frame, availability_status_img, "AVAILABILITY STATUS", availability_status_action)
    create_button(menu_frame, logout_img, "LOGOUT", logout_action)

    # Main content area
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Table header
    header_frame = tk.Frame(main_frame, bg="white")
    header_frame.pack(fill=tk.X)
    headers = ["Date", "Time", "Name", "Reason", "Prescriptions"]
    for header in headers:
        tk.Label(header_frame, text=header, font=("Arial", 12, "bold"), bg="white", borderwidth=2, relief="groove").pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Fetch patient data from the database
    patients = fetch_patients()

    # Table rows
    for row in patients:
        row_frame = tk.Frame(main_frame, bg="white")
        row_frame.pack(fill=tk.X)
        for item in row:
            tk.Label(row_frame, text=item, font=("Arial", 12), bg="white", borderwidth=2, relief="groove").pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Notification button with image
    notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
    notification_btn.place(x=760, y=20)

    root.mainloop()

if __name__ == "__main__":
    create_patient_list_window()

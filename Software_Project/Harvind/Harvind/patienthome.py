import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os

class PatientHomeApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Appointment System")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        self.username = username

        # Image file path
        self.image_path = "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/Images/"

        # Left side menu
        self.menu_frame = tk.Frame(self.root, bg="white")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Main content area
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Welcome text
        self.welcome_label = tk.Label(self.main_frame, text="Welcome", font=("Arial", 24), bg="white")
        self.welcome_label.pack(pady=20)

        # Function to fetch user's full name from the database
        self.fetch_fullname()

        # Load images and create buttons
        self.create_buttons()

        # Appointment history section
        self.history_frame = tk.Frame(self.main_frame, bg="lightblue", padx=10, pady=10)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        past_appointments_label = tk.Label(self.history_frame, text="PAST APPOINTMENTS", bg="lightblue", font=("Arial", 14))
        past_appointments_label.pack(fill=tk.X, pady=(0, 10))

        # Past appointments list (placeholder)
        past_appointments_list = tk.Listbox(self.history_frame)
        past_appointments_list.pack(fill=tk.BOTH, expand=True)

        upcoming_appointments_label = tk.Label(self.history_frame, text="UPCOMING APPOINTMENTS", bg="lightblue", font=("Arial", 14))
        upcoming_appointments_label.pack(fill=tk.X, pady=(10, 0))

        # Upcoming appointments list (placeholder)
        upcoming_appointments_list = tk.Listbox(self.history_frame)
        upcoming_appointments_list.pack(fill=tk.BOTH, expand=True)

        # Notification button with image
        notification_img = self.load_image("bell.png", (30, 30))
        if notification_img:
            notification_btn = tk.Button(self.root, image=notification_img, command=self.notification_action, bg="white", bd=0)
            notification_btn.image = notification_img  # Keep a reference to avoid garbage collection
            notification_btn.place(x=760, y=20)

    def load_image(self, image_name, size):
        try:
            img = Image.open(self.image_path + image_name)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image {image_name}: {e}")
            return None

    def create_buttons(self):
        button_size = (40, 40)
        buttons_info = [
            ("home.png", "HOME", self.home_action),
            ("search.png", "SEARCH/VIEW CLINIC", self.search_view_clinic_action),
            ("sendrequest.png", "SEND REQUEST TO DOCTOR", self.send_request_to_doctor_action),
            ("profile.png", "PROFILE", self.profile_action),
            ("appointment.png", "APPOINTMENT SUMMARY", self.appointment_summary_action),
            ("logout.png", "LOGOUT", self.logout_action)
        ]
        for image_name, text, command in buttons_info:
            image = self.load_image(image_name, button_size)
            if image:
                self.create_button(self.menu_frame, image, text, command)

    def create_button(self, frame, image, text, command):
        btn = tk.Button(frame, image=image, command=command, bg="white", compound=tk.TOP)
        btn.pack(pady=5)
        btn.image = image  # Keep a reference to avoid garbage collection
        label = tk.Label(frame, text=text, bg="white", font=("Arial", 10))
        label.pack()

    def fetch_fullname(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='calladoctor1234',
                database='calladoctor'
            )
            cursor = connection.cursor()
            cursor.execute('''
                SELECT p.fullname FROM users u
                JOIN patients p ON u.user_id = p.user_id
                WHERE u.username = %s
            ''', (self.username,))
            result = cursor.fetchone()
            if result:
                self.update_welcome_label(result[0])
            else:
                messagebox.showerror("Error", "User not found!")
        except Error as e:
            messagebox.showerror("Error", f"Error fetching full name: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_welcome_label(self, fullname):
        self.welcome_label.config(text=f"Welcome {fullname}")

    def home_action(self):
        messagebox.showinfo("Home", "Home Button Clicked")

    def search_view_clinic_action(self):
        messagebox.showinfo("Search/View Clinic", "Search/View Clinic Button Clicked")

    def send_request_to_doctor_action(self):
        messagebox.showinfo("Send Request to Doctor", "Send Request to Doctor Button Clicked")

    def profile_action(self):
        messagebox.showinfo("Profile", "Profile Button Clicked")

    def appointment_summary_action(self):
        messagebox.showinfo("Appointment Summary", "Appointment Summary Button Clicked")

    def logout_action(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()
            os.system('python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/main_page.py"')

    def notification_action(self):
        messagebox.showinfo("Notification", "You have new notifications")

def create_patient_home_window(username):
    root = tk.Tk()
    app = PatientHomeApp(root, username)
    root.mainloop()

if __name__ == "__main__":
    create_patient_home_window("")

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys

# Get admin's full name from command line argument
if len(sys.argv) > 1:
    admin_fullname = sys.argv[1]
else:
    admin_fullname = "ADMIN"

# Function for button actions
def view_clinic_requests():
    messagebox.showinfo("Clinic Requests", "View clinic registration requests clicked")

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

# Create main window
root = tk.Tk()
root.title("Admin Home Page")
root.geometry("800x600")
root.configure(bg="white")

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Load images with specified size
logout_img = load_image("logout.jpg", (40, 40))
notification_img = load_image("bell.jpg", (30, 30))

# Welcome text
welcome_label = tk.Label(root, text=f"Welcome {admin_fullname}", font=("Arial", 24), bg="white")
welcome_label.pack(pady=20)

# Clinic requests section
clinic_requests_frame = tk.Frame(root, bg="white", padx=10, pady=10)
clinic_requests_frame.pack(fill=tk.BOTH, expand=True)

clinic_requests_label = tk.Label(clinic_requests_frame, text="View clinic registration request", font=("Arial", 18), bg="white", borderwidth=2, relief="solid")
clinic_requests_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Set grid column weights for equal column width
clinic_requests_frame.grid_columnconfigure(0, weight=1)
clinic_requests_frame.grid_rowconfigure(0, weight=1)

# Logout button with image
logout_btn = tk.Button(root, image=logout_img, command=logout_action, bg="white", bd=0)
logout_btn.place(x=20, y=520)
logout_label = tk.Label(root, text="LOGOUT", font=("Arial", 12), bg="white")
logout_label.place(x=20, y=560)

# Notification button with image
notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
notification_btn.place(x=760, y=20)

root.mainloop()

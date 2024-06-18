import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image
import customtkinter as ctk
import mysql.connector
import os
import sys

# Get admin's full name from command line argument
if len(sys.argv) > 1:
    admin_fullname = sys.argv[1]
else:
    admin_fullname = "ADMIN"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.LANCZOS)
    return img

# Function for button actions
def view_clinic_requests():
    root.destroy()
    os.system(f'python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/view_clinic_requests.py" "{admin_fullname}"')

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def fetch_registered_clinics():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        query = """
        SELECT clinics.clinic_name, clinics.address, users.fullname 
        FROM clinics 
        JOIN admin_clinics ON clinics.clinic_id = admin_clinics.clinic_id 
        JOIN users ON admin_clinics.user_id = users.user_id 
        WHERE clinics.is_approved = 1
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to fetch data: {error}")
        return []

# Create main window
ctk.set_appearance_mode("light")  # Modes: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Admin Home Page")
root.geometry("800x600")

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Load images with specified size
logout_img = ctk.CTkImage(load_image("logout.png", (40, 40)))

# Welcome text
welcome_label = ctk.CTkLabel(root, text=f"Welcome {admin_fullname}", font=ctk.CTkFont(family="Arial", size=24, weight="bold"))
welcome_label.pack(pady=20)

# Registered clinics title
registered_clinics_label = ctk.CTkLabel(root, text="Registered Clinics", font=ctk.CTkFont(family="Arial", size=18, weight="bold"))
registered_clinics_label.pack(pady=10)

# Registered clinics table
columns = ("Clinic Name", "Clinic Address", "Admin Fullname")
tree = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview")
tree.heading("Clinic Name", text="Clinic Name")
tree.heading("Clinic Address", text="Clinic Address")
tree.heading("Admin Fullname", text="Admin Fullname")

clinics = fetch_registered_clinics()
for clinic in clinics:
    tree.insert("", "end", values=(clinic[0], clinic[1], clinic[2]))

tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Logout button with image
logout_btn = ctk.CTkButton(root, image=logout_img, text="", command=logout_action)
logout_btn.pack(side="left", anchor="s", padx=10, pady=10)

# View clinic requests button
view_requests_btn = ctk.CTkButton(root, text="View clinic registration request", command=view_clinic_requests, font=ctk.CTkFont(family="Arial", size=12))
view_requests_btn.pack(pady=10, padx=10, anchor="se", side=tk.RIGHT)

root.mainloop()

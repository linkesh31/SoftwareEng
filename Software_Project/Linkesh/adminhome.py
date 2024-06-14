import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import os
import sys
import tempfile

# Get admin's full name from command line argument
if len(sys.argv) > 1:
    admin_fullname = sys.argv[1]
else:
    admin_fullname = "ADMIN"

# Function to load and resize images
def load_image(image_name, size):
    img = Image.open(image_path + image_name)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Function for button actions
def view_clinic_requests():
    root.destroy()
    os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/view_clinic_requests.py"')

def logout_action():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.destroy()
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')

def notification_action():
    messagebox.showinfo("Notification", "You have new notifications")

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
        SELECT clinics.clinic_name, clinics.address, clinics.clinic_license, users.fullname 
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

def show_license_image(license_data):
    # Save the binary data to a temporary file and display it
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_file.write(license_data)
    temp_file.close()

    # Function to show the license image
    license_window = tk.Toplevel(root)
    license_window.title("Clinic License")

    img = Image.open(temp_file.name)
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(license_window, image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack()

def on_tree_item_double_click(event):
    # Function to handle double click event on the tree item
    item = tree.selection()[0]
    license_data = tree.item(item, 'values')[2]
    if license_data != 'None':
        show_license_image(license_data)
    else:
        messagebox.showerror("Error", "License image not found.")

# Create main window
root = tk.Tk()
root.title("Admin Home Page")
root.geometry("800x600")
root.configure(bg="white")

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Load images with specified size
logout_img = load_image("logout.jpg", (40, 40))
notification_img = load_image("bell.jpg", (30, 30))

# Welcome text
welcome_label = tk.Label(root, text=f"Welcome {admin_fullname}", font=("Arial", 24), bg="white")
welcome_label.pack(pady=20)

# Registered clinics table
columns = ("Clinic Name", "Clinic Address", "Clinic License", "Admin Fullname")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Clinic Name", text="Clinic Name")
tree.heading("Clinic Address", text="Clinic Address")
tree.heading("Clinic License", text="Clinic License")
tree.heading("Admin Fullname", text="Admin Fullname")

clinics = fetch_registered_clinics()
for clinic in clinics:
    tree.insert("", "end", values=(clinic[0], clinic[1], clinic[2] if clinic[2] else 'None', clinic[3]))

tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
tree.bind("<Double-1>", on_tree_item_double_click)

# Logout button with image
logout_btn = tk.Button(root, image=logout_img, command=logout_action, bg="white", bd=0)
logout_btn.place(x=20, y=520)
logout_label = tk.Label(root, text="LOGOUT", font=("Arial", 12), bg="white")
logout_label.place(x=20, y=560)

# Notification button with image
notification_btn = tk.Button(root, image=notification_img, command=notification_action, bg="white", bd=0)
notification_btn.place(x=760, y=20)

# View clinic requests button
view_requests_btn = tk.Button(root, text="View clinic registration request", command=view_clinic_requests, font=("Arial", 12), bg="lightgray", bd=0)
view_requests_btn.pack(pady=10, padx=10, anchor="se", side=tk.RIGHT)

root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import os

# Function to fetch pending clinics
def fetch_pending_clinics():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        query = "SELECT clinic_id, clinic_name, address, clinic_license FROM clinics WHERE is_approved = 0"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to fetch data: {error}")
        return []

# Function to approve clinic
def approve_clinic():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please choose a clinic to approve.")
        return

    clinic_id = tree.item(selected_item)['values'][0]
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        query = "UPDATE clinics SET is_approved = 1 WHERE clinic_id = %s"
        cursor.execute(query, (clinic_id,))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Clinic approved successfully!")
        refresh_table()
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to approve clinic: {error}")

# Function to reject clinic
def reject_clinic():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please choose a clinic to reject.")
        return

    clinic_id = tree.item(selected_item)['values'][0]
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        query = "DELETE FROM clinics WHERE clinic_id = %s"
        cursor.execute(query, (clinic_id,))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Clinic rejected successfully!")
        refresh_table()
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"Failed to reject clinic: {error}")

# Function to refresh the table
def refresh_table():
    for item in tree.get_children():
        tree.delete(item)
    pending_clinics = fetch_pending_clinics()
    for clinic in pending_clinics:
        tree.insert("", "end", values=clinic)

# Function for back button
def back_to_home():
    root.destroy()
    os.system('python "C:/Users/user/Documents/GitHub/SoftwareEng/Software_Project/Harvind/adminhome.py"')

# Create main window
root = tk.Tk()
root.title("Pending Clinic Registrations")
root.geometry("800x600")
root.configure(bg="white")

# Table for pending clinics
columns = ("Clinic ID", "Clinic Name", "Clinic Address", "Clinic License")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Clinic ID", text="Clinic ID")
tree.heading("Clinic Name", text="Clinic Name")
tree.heading("Clinic Address", text="Clinic Address")
tree.heading("Clinic License", text="Clinic License")

refresh_table()

tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Approve button
approve_btn = tk.Button(root, text="Approve", command=approve_clinic, font=("Arial", 12), bg="lightgray", bd=0)
approve_btn.pack(side=tk.LEFT, padx=20, pady=20)

# Reject button
reject_btn = tk.Button(root, text="Reject", command=reject_clinic, font=("Arial", 12), bg="lightgray", bd=0)
reject_btn.pack(side=tk.LEFT, padx=20, pady=20)

# Back button
back_btn = tk.Button(root, text="Back", command=back_to_home, font=("Arial", 12), bg="lightgray", bd=0)
back_btn.pack(side=tk.RIGHT, padx=20, pady=20)

root.mainloop()
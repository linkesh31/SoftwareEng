import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import os
import sys

# Get clinic ID and admin full name from command line arguments
if len(sys.argv) > 2:
    clinic_id = sys.argv[1]
    admin_fullname = sys.argv[2]
else:
    clinic_id = None
    admin_fullname = "ADMIN"

# Debug: Print received command-line arguments
print(f"Debug: Received clinic_id = {clinic_id}, admin_fullname = {admin_fullname}")

# Function to validate and save the new doctor's information to the database
def save_doctor():
    fullname = fullname_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    gender = gender_combobox.get()
    ic = ic_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()
    year = year_combobox.get()
    month = month_combobox.get()
    day = day_combobox.get()

    if not (fullname and username and password and confirm_password and gender and ic and email and phone and address and year and month and day):
        messagebox.showerror("Error", "Please fill all the fields.")
        return

    if year == "Year":
        messagebox.showerror("Error", "Please fill in the year column.")
        return

    if month == "Month":
        messagebox.showerror("Error", "Please fill in the month column.")
        return

    if day == "Day":
        messagebox.showerror("Error", "Please fill in the day column.")
        return

    dob = f"{year}-{month}-{day}"

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()

        # Ensure clinic_id is assigned correctly
        global clinic_id
        if clinic_id is None:
            cursor.execute('''
                SELECT admin_clinics.clinic_id 
                FROM admin_clinics 
                JOIN users ON admin_clinics.admin_id = users.user_id 
                WHERE users.fullname = %s
            ''', (admin_fullname,))
            clinic_id_result = cursor.fetchone()
            print(f"Debug: SQL query executed with admin_fullname = {admin_fullname}")  # Debug print statement
            if clinic_id_result:
                clinic_id = clinic_id_result[0]
                print(f"Debug: Retrieved clinic_id = {clinic_id}")  # Debug print statement
            else:
                messagebox.showerror("Error", "Clinic ID not found.")
                print("Debug: Clinic ID not found.")  # Debug print statement
                return

        cursor.execute('''
            INSERT INTO users (username, password, email, phone_number, fullname, role, date_of_birth, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (username, password, email, phone, fullname, 'doctor', dob, address))
        user_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO doctors (user_id, fullname, clinic_id, is_available, gender, identification_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (user_id, fullname, clinic_id, 1, gender, ic))
        connection.commit()
        messagebox.showinfo("Success", "Doctor added successfully!")
        root.destroy()
        os.system(f'python clinicadminhome.py {clinic_id} {admin_fullname}')
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def back_action():
    root.destroy()
    os.system(f'python clinicadminhome.py {clinic_id} {admin_fullname}')

# Validation function for IC entry
def limit_ic_length(*args):
    value = ic_var.get()
    if len(value) > 12:
        ic_var.set(value[:12])

# Create main window
root = tk.Tk()
root.title("Add Doctor")
root.geometry("800x600")
root.configure(bg="lightblue")

# Title label
title_label = tk.Label(root, text="Add Doctor", font=("Helvetica", 24, "bold"), bg="lightblue")
title_label.pack(pady=10)

# Frame for form
form_frame = tk.Frame(root, bg="lightblue")
form_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Form fields
labels = ["Fullname:", "Username:", "Password:", "Confirm Password:", "Gender:", "IC(without dash):", "Email:", "Phone:", "Address:"]
entries = {}

for i, label_text in enumerate(labels):
    label = tk.Label(form_frame, text=label_text, font=("Helvetica", 14), bg="lightblue")
    label.grid(row=i, column=0, sticky="e", pady=5, padx=5)
    if label_text == "Gender:":
        entry = ttk.Combobox(form_frame, font=("Helvetica", 14), values=["Male", "Female", "Rather not to say"])
        entry.current(0)  # Set default value
    else:
        entry = tk.Entry(form_frame, font=("Helvetica", 14), show="*" if "Password" in label_text else "")
    entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")
    entries[label_text] = entry

# Add date of birth fields
dob_label = tk.Label(form_frame, text="Date of Birth:", font=("Helvetica", 14), bg="lightblue")
dob_label.grid(row=len(labels), column=0, sticky="e", pady=5, padx=5)

# Adjust the width of Combobox for Year, Month, and Day
dob_frame = tk.Frame(form_frame, bg="lightblue")
dob_frame.grid(row=len(labels), column=1, pady=5, padx=5, sticky="w")

year_combobox = ttk.Combobox(dob_frame, font=("Helvetica", 14), values=[str(year) for year in range(1900, 2025)], width=5)
year_combobox.pack(side=tk.LEFT)
year_combobox.set("Year")

month_combobox = ttk.Combobox(dob_frame, font=("Helvetica", 14), values=[f"{month:02d}" for month in range(1, 13)], width=3)
month_combobox.pack(side=tk.LEFT, padx=(5, 0))
month_combobox.set("Month")

day_combobox = ttk.Combobox(dob_frame, font=("Helvetica", 14), values=[f"{day:02d}" for day in range(1, 32)], width=3)
day_combobox.pack(side=tk.LEFT, padx=(5, 0))
day_combobox.set("Day")

# Save button
save_button = tk.Button(root, text="Save", command=save_doctor, bg="lightblue", font=("Helvetica", 12))
save_button.pack(pady=20)

# Back button
back_button = tk.Button(root, text="Back", command=back_action, bg="lightblue", font=("Helvetica", 12))
back_button.pack(side=tk.BOTTOM, pady=20)

# Unpack entries for easier access
fullname_entry = entries["Fullname:"]
username_entry = entries["Username:"]
password_entry = entries["Password:"]
confirm_password_entry = entries["Confirm Password:"]
gender_combobox = entries["Gender:"]
ic_entry = entries["IC(without dash):"]
email_entry = entries["Email:"]
phone_entry = entries["Phone:"]
address_entry = entries["Address:"]

# Set up IC entry variable and trace for validation
ic_var = tk.StringVar()
ic_var.trace_add("write", limit_ic_length)
ic_entry.config(textvariable=ic_var)

root.mainloop()

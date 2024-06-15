import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import mysql.connector
import subprocess
import sys

def get_available_doctors(clinic_id, selected_date, selected_time):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()

        query = """
        SELECT d.fullname
        FROM doctors d
        LEFT JOIN appointments a
        ON d.doctor_id = a.doctor_id
        AND a.appointment_date = %s
        AND a.appointment_time = %s
        WHERE d.clinic_id = %s
        AND (a.appointment_id IS NULL OR a.appointment_request_status != 'accepted')
        """

        cursor.execute(query, (selected_date, selected_time, clinic_id))
        available_doctors = cursor.fetchall()

        connection.close()
        return available_doctors
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

def search_doctors():
    selected_date = date_entry.get_date().strftime('%Y-%m-%d')
    selected_time = time_entry.get()

    if not selected_time:
        messagebox.showwarning("Input Error", "Please select a time.")
        return

    available_doctors = get_available_doctors(clinic_id, selected_date, selected_time)

    for row in tree.get_children():
        tree.delete(row)

    if not available_doctors:
        messagebox.showinfo("No Doctors Available", "No doctors are available for the selected date and time.")
    else:
        for doctor in available_doctors:
            tree.insert("", "end", values=doctor)

def back_action():
    root.destroy()
    subprocess.run(['python', 'adminclinichome.py', clinic_id, admin_fullname])

# Main window
root = tk.Tk()
root.title("Appointment Schedule")
root.geometry("600x600")
root.configure(bg="white")

# Retrieve clinic ID and admin full name from command line arguments
if len(sys.argv) > 2:
    clinic_id = sys.argv[1]
    admin_fullname = sys.argv[2]
else:
    clinic_id = "Unknown Clinic"
    admin_fullname = "ADMIN"

# Date selection
date_label = tk.Label(root, text="Select Date:", font=("Arial", 12), bg="white")
date_label.pack(pady=10)
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024, month=6, day=15, date_pattern='yyyy-mm-dd')
date_entry.pack(pady=10)

# Time selection
time_label = tk.Label(root, text="Select Time:", font=("Arial", 12), bg="white")
time_label.pack(pady=10)
time_options = ["08:00:00", "09:00:00", "10:00:00", "11:00:00", "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00"]
time_entry = ttk.Combobox(root, values=time_options, font=("Arial", 12))
time_entry.pack(pady=10)

# Search button
search_button = tk.Button(root, text="Search", command=search_doctors, font=("Arial", 12), bg="lightblue")
search_button.pack(pady=20)

# Treeview for displaying available doctors
tree = ttk.Treeview(root, columns=("Doctor",), show='headings', height=8)
tree.heading("Doctor", text="Doctor")
tree.pack(pady=20)

# Back button
back_button = tk.Button(root, text="Back", command=back_action, font=("Arial", 12), bg="lightgrey")
back_button.pack(pady=20)

root.mainloop()

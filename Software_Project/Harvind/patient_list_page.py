import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error

# Database connection function
def create_connection(host='localhost', username='root', password='calladoctor1234', database='calladoctor'):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=database
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to view past patient report
def view_report(appointment_id):
    messagebox.showinfo("View Report", f"Viewing report for appointment ID {appointment_id}")

# Function to generate report for upcoming patient
def generate_report(appointment_id):
    messagebox.showinfo("Generate Report", f"Generating report for appointment ID {appointment_id}")

# Function to display the list of patients
def display_patient_list():
    root = tk.Tk()
    root.title("List of Patients")
    root.geometry("800x600")

    # Create a frame for the list
    list_frame = tk.Frame(root, bg="white")
    list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Create and place the table headings
    headings = ["Date", "Time", "Name", "Reason", "Prescriptions"]
    for col, heading in enumerate(headings):
        label = tk.Label(list_frame, text=heading, font=("Arial", 12, "bold"), bg="white", borderwidth=2, relief="groove")
        label.grid(row=0, column=col, sticky="nsew")

    # Query the database for patient appointments
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT a.appointment_date, p.fullname, a.appointment_type, a.status, a.appointment_id
    FROM Appointments a
    JOIN Patients p ON a.patient_id = p.patient_id
    WHERE a.doctor_id = (SELECT doctor_id FROM Doctors WHERE user_id = (SELECT user_id FROM Users WHERE username = 'DR.LINKESH'))"""
    cursor.execute(query)
    appointments = cursor.fetchall()

    # Display appointments
    for row_num, appointment in enumerate(appointments, start=1):
        appointment_date, fullname, appointment_type, status, appointment_id = appointment
        date_str = appointment_date.strftime("%d/%m/%Y")
        time_str = appointment_date.strftime("%I:%M%p")

        date_label = tk.Label(list_frame, text=date_str, font=("Arial", 10), fg="red" if status == 'completed' else "green", bg="white", borderwidth=2, relief="groove")
        date_label.grid(row=row_num, column=0, sticky="nsew")

        time_label = tk.Label(list_frame, text=time_str, font=("Arial", 10), fg="red" if status == 'completed' else "green", bg="white", borderwidth=2, relief="groove")
        time_label.grid(row=row_num, column=1, sticky="nsew")

        name_label = tk.Label(list_frame, text=fullname, font=("Arial", 10), fg="red" if status == 'completed' else "green", bg="white", borderwidth=2, relief="groove")
        name_label.grid(row=row_num, column=2, sticky="nsew")

        reason_label = tk.Label(list_frame, text=appointment_type, font=("Arial", 10), fg="red" if status == 'completed' else "green", bg="white", borderwidth=2, relief="groove")
        reason_label.grid(row=row_num, column=3, sticky="nsew")

        # Prescription icons
        view_icon = tk.PhotoImage(file="view.png")  # Load view icon
        generate_icon = tk.PhotoImage(file="generate.png")  # Load generate icon

        if status == 'completed':
            btn = tk.Button(list_frame, image=view_icon, command=lambda aid=appointment_id: view_report(aid), bg="white")
        else:
            btn = tk.Button(list_frame, image=generate_icon, command=lambda aid=appointment_id: generate_report(aid), bg="white")

        btn.image = view_icon if status == 'completed' else generate_icon  # Keep a reference to avoid garbage collection
        btn.grid(row=row_num, column=4, sticky="nsew")

    connection.close()
    root.mainloop()

if __name__ == "__main__":
    display_patient_list()
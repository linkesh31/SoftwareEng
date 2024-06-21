import customtkinter as ctk  # Importing customtkinter module and aliasing it as ctk for creating custom-styled tkinter widgets.
from tkinter import messagebox, ttk  # Importing messagebox and ttk (themed tkinter widgets) from tkinter.
from PIL import Image, ImageTk  # Importing Image and ImageTk from the PIL (Python Imaging Library) for image handling.
import mysql.connector  # Importing mysql.connector for connecting to and interacting with MySQL databases.
import os  # Importing os module for interacting with the operating system.
import sys  # Importing sys module for system-specific parameters and functions.
import subprocess  # Importing subprocess module to run new applications or programs from the Python script.

# Function to fetch doctor's full name
def get_doctor_fullname(doctor_id):
    """Fetch the full name of the doctor based on the provided doctor ID."""
    try:
        db = mysql.connector.connect(
            host="localhost",  # Database host.
            user="root",  # Database user.
            password="calladoctor1234",  # Database password.
            database="calladoctor"  # Database name.
        )
        cursor = db.cursor()  # Creating a cursor object to execute SQL queries.
        cursor.execute("SELECT fullname FROM doctors WHERE doctor_id = %s", (doctor_id,))  # SQL query to get the doctor's full name.
        result = cursor.fetchone()  # Fetching the result of the query.
        db.close()  # Closing the database connection.
        if result:  # Checking if a result was found.
            return result[0]  # Returning the doctor's full name.
        else:  # If no result is found.
            raise ValueError(f"No doctor found with ID {doctor_id}")  # Raise a ValueError with an appropriate message.
    except mysql.connector.Error as err:  # Catching any MySQL database errors.
        print(f"Database Error: {err}")  # Printing the error message.
        messagebox.showerror("Database Error", f"Error: {err}")  # Showing an error message box.
        return "Doctor"  # Returning a default value if an error occurs.

# Function to fetch appointments
def fetch_appointments(doctor_id):
    """Fetch past and upcoming appointments for the specified doctor."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Database host.
            user="root",  # Database user.
            password="calladoctor1234",  # Database password.
            database="calladoctor"  # Database name.
        )
        cursor = connection.cursor()  # Creating a cursor object to execute SQL queries.

        # Fetch past appointments
        cursor.execute("""
            SELECT a.appointment_date, a.appointment_time, p.fullname, a.reason, IFNULL(pr.medical_report, 'N/A')
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            LEFT JOIN prescriptions pr ON a.appointment_id = pr.appointment_id
            WHERE a.doctor_id = %s AND a.treatment_status = 'done'
            ORDER BY a.appointment_date DESC
        """, (doctor_id,))
        past_appointments = cursor.fetchall()  # Fetching all results of the query.

        # Fetch upcoming appointments
        cursor.execute("""
            SELECT a.appointment_id, a.appointment_date, a.appointment_time, p.fullname, a.reason
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = %s AND a.treatment_status = 'pending' AND a.appointment_request_status = 'accepted'
            ORDER BY a.appointment_date ASC
        """, (doctor_id,))
        upcoming_appointments = cursor.fetchall()  # Fetching all results of the query.

        cursor.close()  # Closing the cursor.
        connection.close()  # Closing the database connection.

        return past_appointments, upcoming_appointments  # Returning the fetched past and upcoming appointments.
    except mysql.connector.Error as e:  # Catching any MySQL database errors.
        print(f"The error '{e}' occurred")  # Printing the error message.
        return [], []  # Returning empty lists if an error occurs.

# Function to create prescription form and save the prescription
def create_prescription_form(appointment_id, doctor_id, patient_name):
    """Create a form for entering a prescription and save it to the database."""
    def save_prescription():
        """Save the prescription to the database."""
        prescription = text.get("1.0", ctk.END).strip()  # Getting the entered prescription text from the textbox.
        if prescription:  # Checking if the prescription is not empty.
            response = messagebox.askyesno("Confirmation", "This will result in completing the patient's appointment. Do you want to proceed?")  # Asking for confirmation to proceed.
            if response:  # If the user confirms.
                try:
                    connection = mysql.connector.connect(
                        host="localhost",  # Database host.
                        user="root",  # Database user.
                        password="calladoctor1234",  # Database password.
                        database="calladoctor"  # Database name.
                    )
                    cursor = connection.cursor()  # Creating a cursor object to execute SQL queries.
                    cursor.execute("""
                        INSERT INTO prescriptions (appointment_id, doctor_id, patient_id, medical_report)
                        VALUES (%s, %s, (SELECT patient_id FROM appointments WHERE appointment_id = %s), %s)
                    """, (appointment_id, doctor_id, appointment_id, prescription))  # SQL query to insert the prescription into the database.
                    cursor.execute("""
                        UPDATE appointments
                        SET treatment_status = 'done'
                        WHERE appointment_id = %s
                    """, (appointment_id,))  # SQL query to update the appointment's treatment status to 'done'.
                    connection.commit()  # Committing the transaction.
                    cursor.close()  # Closing the cursor.
                    connection.close()  # Closing the database connection.
                    refresh_appointments()  # Refreshing the appointments list.
                    messagebox.showinfo("Success", "Prescription saved successfully.")  # Showing a success message.
                    prescription_window.destroy()  # Closing the prescription window.
                    root.deiconify()  # Re-enabling the main window.
                except mysql.connector.Error as err:  # Catching any MySQL database errors.
                    print(f"Database Error: {err}")  # Printing the error message.
                    messagebox.showerror("Database Error", f"Error: {err}")  # Showing an error message box.
        else:  # If the prescription is empty.
            messagebox.showwarning("Warning", "Prescription cannot be empty.")  # Showing a warning message.

    def go_back():
        """Close the prescription window and go back to the main window."""
        prescription_window.destroy()  # Closing the prescription window.
        root.deiconify()  # Re-enabling the main window.

    root.withdraw()  # Disabling the main window.

    prescription_window = ctk.CTkToplevel(root)  # Creating a new top-level window for the prescription form.
    prescription_window.title("Prescription")  # Setting the title of the prescription window.
    prescription_window.geometry("400x250")  # Setting the size of the prescription window.

    label = ctk.CTkLabel(prescription_window, text=f"Enter Prescription for {patient_name}:")  # Creating a label for the prescription textbox.
    label.pack(pady=10)  # Packing the label with some padding.
    text = ctk.CTkTextbox(prescription_window, height=90, width=180)  # Creating a textbox for entering the prescription.
    text.pack(pady=10)  # Packing the textbox with some padding.

    button_frame = ctk.CTkFrame(prescription_window)  # Creating a frame to hold the buttons.
    button_frame.pack(pady=10)  # Packing the button frame with some padding.

    save_button = ctk.CTkButton(button_frame, text="Save", command=save_prescription)  # Creating a button to save the prescription.
    save_button.pack(side=ctk.LEFT, padx=5)  # Packing the save button with some padding.

    back_button = ctk.CTkButton(button_frame, text="Back", command=go_back)  # Creating a button to go back to the main window.
    back_button.pack(side=ctk.LEFT, padx=5)  # Packing the back button with some padding.

# Function for button actions
def profile_action():
    """Destroy the main window and run the doctor profile script."""
    root.destroy()  # Destroy the main window.
    subprocess.run(['python', 'doctorprofile.py', str(doctor_id)])  # Run the doctor profile script with the doctor_id as an argument.

def logout_action():
    """Prompt for confirmation and logout if confirmed."""
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")  # Asking for confirmation to logout.
    if response:  # If the user confirms.
        root.destroy()  # Destroy the main window.
        os.system('python "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/main_page.py"')  # Run the main page script.

# Function to refresh the appointments table
def refresh_appointments():
    """Fetch and display past and upcoming appointments."""
    past_appointments, upcoming_appointments = fetch_appointments(doctor_id)  # Fetch appointments for the doctor.

    for widget in past_appointments_frame.winfo_children():  # Clear existing entries in the past appointments frame.
        widget.destroy()
    for widget in upcoming_appointments_frame.winfo_children():  # Clear existing entries in the upcoming appointments frame.
        widget.destroy()

    past_columns = ["Date", "Time", "Patient Name", "Reason", "Prescription"]  # Define columns for past appointments.
    for col in past_columns:  # Iterate through the columns.
        header = ctk.CTkLabel(past_appointments_frame, text=col, font=("Arial", 14, "bold"), fg_color="#E0F7FA", padx=5, pady=5)  # Create a header label for each column.
        header.grid(row=0, column=past_columns.index(col), sticky="nsew")  # Grid layout for the header.

    for i, appointment in enumerate(past_appointments):  # Iterate through past appointments.
        for j, value in enumerate(appointment):  # Iterate through values in each appointment.
            label = ctk.CTkLabel(past_appointments_frame, text=value, font=("Arial", 12), fg_color="white", padx=5, pady=5)  # Create a label for each value.
            label.grid(row=i + 1, column=j, sticky="nsew")  # Grid layout for the label.

    for col in range(len(past_columns)):  # Configure grid columns for past appointments.
        past_appointments_frame.grid_columnconfigure(col, weight=1)

    upcoming_columns = ["Date", "Time", "Patient Name", "Reason", "Action"]  # Define columns for upcoming appointments.
    for col in upcoming_columns:  # Iterate through the columns.
        header = ctk.CTkLabel(upcoming_appointments_frame, text=col, font=("Arial", 14, "bold"), fg_color="#E0F7FA", padx=5, pady=5)  # Create a header label for each column.
        header.grid(row=0, column=upcoming_columns.index(col), sticky="nsew")  # Grid layout for the header.

    for i, appointment in enumerate(upcoming_appointments):  # Iterate through upcoming appointments.
        appointment_id, date, time, patient_name, reason = appointment  # Unpack appointment details.
        for j, value in enumerate(appointment[1:]):  # Iterate through values in each appointment.
            label = ctk.CTkLabel(upcoming_appointments_frame, text=value, font=("Arial", 12), fg_color="white", padx=5, pady=5)  # Create a label for each value.
            label.grid(row=i + 1, column=j, sticky="nsew")  # Grid layout for the label.
        prescribe_button = ctk.CTkButton(upcoming_appointments_frame, text="Generate prescription",  # Create a button to generate prescription.
                                         command=lambda appt_id=appointment_id, pt_name=patient_name: create_prescription_form(appt_id, doctor_id, pt_name),  # Lambda function to pass arguments to create_prescription_form.
                                         fg_color="blue", text_color="white", font=("Arial", 10))  # Button styling.
        prescribe_button.grid(row=i + 1, column=len(appointment[1:]), sticky="nsew")  # Grid layout for the button.

    for col in range(len(upcoming_columns)):  # Configure grid columns for upcoming appointments.
        upcoming_appointments_frame.grid_columnconfigure(col, weight=1)

# Get doctor_id from command-line arguments
doctor_id = sys.argv[1] if len(sys.argv) > 1 else None  # Get doctor_id from command line arguments.
if doctor_id:  # Check if doctor_id is provided.
    try:
        doctor_id = int(doctor_id)  # Convert doctor_id to integer.
        doctor_fullname = get_doctor_fullname(doctor_id)  # Fetch doctor's full name based on doctor_id.
    except ValueError as ve:  # Catch ValueError if doctor_id is not an integer.
        print(f"ValueError: {ve}")  # Print the error message.
        doctor_fullname = "Unknown Doctor"  # Set a default name.
else:  # If doctor_id is not provided.
    doctor_fullname = "Unknown Doctor"  # Set a default name.

# Create main window
ctk.set_appearance_mode("light")  # Set appearance mode to light.
ctk.set_default_color_theme("blue")  # Set default color theme to blue.

root = ctk.CTk()  # Create the main tkinter window.
root.title("Doctor Home Page")  # Set the title of the main window.
root.geometry("1000x700")  # Set the size of the main window.
root.configure(fg_color="#AED6F1")  # Set the background color of the main window.

# Image file path
image_path = "C:/Users/linke/OneDrive/Documents/GitHub/SoftwareEng/Software_Project/Linkesh/Images/"

# Function to load and resize images
def load_image(image_name, size):
    """Load and resize images."""
    img = Image.open(image_path + image_name)  # Open the image file.
    img = img.resize(size, Image.Resampling.LANCZOS)  # Resize the image.
    return ctk.CTkImage(light_image=img, size=size)  # Return a custom tkinter image.

# Load images with specified size
button_size = (40, 40)  # Specify the size of the buttons.
profile_img = load_image("profile.png", button_size)  # Load and resize profile image.
logout_img = load_image("logout.png", button_size)  # Load and resize logout image.

# Left side menu
menu_frame = ctk.CTkFrame(root, fg_color="#E6E6FA")  # Create a frame for the menu.
menu_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)  # Pack the menu frame.

# Menu buttons with images and labels
def create_button(frame, image, text, command):
    """Create a button with image and label."""
    button_frame = ctk.CTkFrame(frame, fg_color="#E6E6FA")  # Create a frame for the button.
    button_frame.pack(fill=ctk.X, pady=5, padx=5)  # Pack the button frame.
    btn = ctk.CTkButton(button_frame, image=image, command=command, fg_color="white", hover_color="#AED6F1", text="")  # Create a button with image and command.
    btn.pack(pady=0)  # Pack the button.
    label = ctk.CTkLabel(button_frame, text=text, fg_color="#E6E6FA", font=("Arial", 12, "bold"))  # Create a label for the button.
    label.pack(pady=5)  # Pack the label.
    return button_frame  # Return the button frame.

create_button(menu_frame, profile_img, "PROFILE", profile_action)  # Create profile button.
create_button(menu_frame, logout_img, "LOGOUT", logout_action)  # Create logout button.

# Main content area
main_frame = ctk.CTkFrame(root, fg_color="#AED6F1")  # Create a frame for the main content.
main_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)  # Pack the main content frame.

# Welcome text
welcome_label = ctk.CTkLabel(main_frame, text=f"Welcome DR. {doctor_fullname}", font=("Arial", 24), fg_color="#AED6F1")  # Create a label for the welcome text.
welcome_label.pack(pady=20)  # Pack the welcome label.

# Past appointments section
past_appointments_label = ctk.CTkLabel(main_frame, text="PAST APPOINTMENTS", fg_color="#AED6F1", font=("Arial", 18))  # Create a label for past appointments.
past_appointments_label.pack(fill=ctk.X, pady=(0, 10))  # Pack the past appointments label.

past_appointments_frame = ctk.CTkFrame(main_frame, fg_color="white")  # Create a frame for past appointments.
past_appointments_frame.pack(fill=ctk.BOTH, expand=True)  # Pack the past appointments frame.

# Upcoming appointments section
upcoming_appointments_label = ctk.CTkLabel(main_frame, text="UPCOMING APPOINTMENTS", fg_color="#AED6F1", font=("Arial", 18))  # Create a label for upcoming appointments.
upcoming_appointments_label.pack(fill=ctk.X, pady=(10, 0))  # Pack the upcoming appointments label.

upcoming_appointments_frame = ctk.CTkFrame(main_frame, fg_color="white")  # Create a frame for upcoming appointments.
upcoming_appointments_frame.pack(fill=ctk.BOTH, expand=True)  # Pack the upcoming appointments frame.

# Fetch appointment data for the specific doctor
refresh_appointments()  # Fetch and display appointments.

root.mainloop()  # Run the main tkinter event loop.

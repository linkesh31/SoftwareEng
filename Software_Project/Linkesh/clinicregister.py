import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error

def submit_clinic_data(clinic_name, clinic_address, clinic_license_path, admin_fullname, admin_username, admin_password, admin_email, admin_phone_number, admin_date_of_birth, admin_address):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()

        # Insert clinic data
        with open(clinic_license_path, 'rb') as f:
            clinic_license_data = f.read()
        insert_clinic_query = """INSERT INTO clinics (clinic_name, address, clinic_license) VALUES (%s, %s, %s)"""
        clinic_data = (clinic_name, clinic_address, clinic_license_data)
        cursor.execute(insert_clinic_query, clinic_data)
        clinic_id = cursor.lastrowid

        # Insert user data
        insert_user_query = """INSERT INTO users (username, password, email, phone_number, date_of_birth, address, role, fullname) VALUES (%s, %s, %s, %s, %s, %s, 'clinic_admin', %s)"""
        user_data = (admin_username, admin_password, admin_email, admin_phone_number, admin_date_of_birth, admin_address, admin_fullname)
        cursor.execute(insert_user_query, user_data)
        user_id = cursor.lastrowid

        # Link admin to clinic
        insert_admin_clinic_query = """INSERT INTO admin_clinics (admin_id, clinic_id, user_id) VALUES (%s, %s, %s)"""
        admin_clinic_data = (user_id, clinic_id, user_id)
        cursor.execute(insert_admin_clinic_query, admin_clinic_data)

        connection.commit()
        messagebox.showinfo("Success", "Request for clinic registration has been sent! Wait for approval.")
        clinic_register_root.destroy()
        import main_page
        main_page.create_login_window()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to register clinic: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"), ("All files", "*.*")])
    return filename

def create_clinic_register_window():
    global clinic_register_root, clinic_license_path
    clinic_license_path = None  # Initialize the variable to store the file path
    clinic_register_root = ctk.CTk()
    clinic_register_root.title("Clinic Registration")
    width = 600
    height = 750
    clinic_register_root.geometry(f"{width}x{height}")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    top_frame = ctk.CTkFrame(clinic_register_root)
    top_frame.pack(fill="both", expand=True)

    title_label = ctk.CTkLabel(top_frame, text="Call a Doctor", font=("Helvetica", 24, "bold"), text_color="black")
    title_label.pack(pady=10)

    sub_title_label = ctk.CTkLabel(top_frame, text="Welcome to Registration", font=("Helvetica", 18), text_color="black")
    sub_title_label.pack(pady=10)

    form_frame = ctk.CTkFrame(top_frame)
    form_frame.pack(pady=10)

    # Clinic info section
    clinic_info_label = ctk.CTkLabel(form_frame, text="Clinic info", font=("Helvetica", 16), text_color="black")
    clinic_info_label.grid(row=0, column=0, columnspan=2, pady=1)

    clinic_name_label = ctk.CTkLabel(form_frame, text="Clinic Name:", font=("Helvetica", 14), text_color="black")
    clinic_name_label.grid(row=1, column=0, sticky="e", pady=5)
    clinic_name_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black")
    clinic_name_entry.grid(row=1, column=1, pady=5)

    clinic_address_label = ctk.CTkLabel(form_frame, text="Clinic Address:", font=("Helvetica", 14), text_color="black")
    clinic_address_label.grid(row=2, column=0, sticky="e", pady=5)
    clinic_address_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black")
    clinic_address_entry.grid(row=2, column=1, pady=5)

    clinic_license_label = ctk.CTkLabel(form_frame, text="Clinic License:", font=("Helvetica", 14), text_color="black")
    clinic_license_label.grid(row=3, column=0, sticky="e", pady=5)
    clinic_license_button = ctk.CTkButton(form_frame, text="Choose File", font=("Helvetica", 12), command=lambda: choose_file(clinic_license_path_label))
    clinic_license_button.grid(row=3, column=1, pady=5)
    clinic_license_path_label = ctk.CTkLabel(form_frame, text="", font=("Helvetica", 12), text_color="black")
    clinic_license_path_label.grid(row=4, column=0, columnspan=2, pady=5)

    def choose_file(label):
        global clinic_license_path
        path = browse_file()
        if path:
            clinic_license_path = path  # Store the selected file path
            label.configure(text="File uploaded successfully")

    # Clinic admin info section
    clinic_admin_info_label = ctk.CTkLabel(form_frame, text="Clinic Admin info", font=("Helvetica", 16), text_color="black")
    clinic_admin_info_label.grid(row=5, column=0, columnspan=2, pady=5)

    fullname_label = ctk.CTkLabel(form_frame, text="Fullname:", font=("Helvetica", 14), text_color="black")
    fullname_label.grid(row=6, column=0, sticky="e", pady=5)
    fullname_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black")
    fullname_entry.grid(row=6, column=1, pady=5)

    email_label = ctk.CTkLabel(form_frame, text="Email:", font=("Helvetica", 14), text_color="black")
    email_label.grid(row=7, column=0, sticky="e", pady=5)
    email_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black")
    email_entry.grid(row=7, column=1, pady=5)

    username_label = ctk.CTkLabel(form_frame, text="Username:", font=("Helvetica", 14), text_color="black")
    username_label.grid(row=8, column=0, sticky="e", pady=5)
    username_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black")
    username_entry.grid(row=8, column=1, pady=5)

    password_label = ctk.CTkLabel(form_frame, text="Password:", font=("Helvetica", 14), text_color="black")
    password_label.grid(row=9, column=0, sticky="e", pady=5)
    password_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black", show="*")
    password_entry.grid(row=9, column=1, pady=5)

    confirm_password_label = ctk.CTkLabel(form_frame, text="Confirm Password:", font=("Helvetica", 14), text_color="black")
    confirm_password_label.grid(row=10, column=0, sticky="e", pady=5)
    confirm_password_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black", show="*")
    confirm_password_entry.grid(row=10, column=1, pady=5)

    phone_number_label = ctk.CTkLabel(form_frame, text="Phone Number:", font=("Helvetica", 14), text_color="black")
    phone_number_label.grid(row=11, column=0, sticky="e", pady=5)
    phone_number_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black")
    phone_number_entry.grid(row=11, column=1, pady=5)

    admin_address_label = ctk.CTkLabel(form_frame, text="Admin Address:", font=("Helvetica", 14), text_color="black")
    admin_address_label.grid(row=12, column=0, sticky="e", pady=5)
    admin_address_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 14), fg_color="white", text_color="black")
    admin_address_entry.grid(row=12, column=1, pady=5)

    date_of_birth_label = ctk.CTkLabel(form_frame, text="Date of Birth:", font=("Helvetica", 14), text_color="black")
    date_of_birth_label.grid(row=13, column=0, sticky="e", pady=5)
    date_of_birth_entry = DateEntry(form_frame, font=("Helvetica", 14), date_pattern='y-mm-dd')
    date_of_birth_entry.grid(row=13, column=1, pady=5)

    def on_register_click():
        clinic_name = clinic_name_entry.get()
        clinic_address = clinic_address_entry.get()
        admin_fullname = fullname_entry.get()
        admin_username = username_entry.get()
        admin_password = password_entry.get()
        admin_email = email_entry.get()
        admin_phone_number = phone_number_entry.get()
        admin_address = admin_address_entry.get()
        admin_date_of_birth = date_of_birth_entry.get()

        # Validate that all fields are filled
        if not clinic_name or not clinic_address or not admin_fullname or not admin_username or not admin_password or not admin_email or not admin_phone_number or not admin_address:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Validate phone number
        if not admin_phone_number.isdigit():
            messagebox.showerror("Error", "Phone number must contain only digits.")
            return

        # Validate password match
        if admin_password != confirm_password_entry.get():
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Validate that a file was chosen
        if not clinic_license_path:
            messagebox.showerror("Error", "Please upload a clinic license file.")
            return

        submit_clinic_data(clinic_name, clinic_address, clinic_license_path, admin_fullname, admin_username, admin_password, admin_email, admin_phone_number, admin_date_of_birth, admin_address)

    register_button = ctk.CTkButton(form_frame, text="Register", font=("Helvetica", 14), command=on_register_click)
    register_button.grid(row=14, column=0, columnspan=2, pady=10)

    def on_back_click():
        clinic_register_root.destroy()
        import register_page
        register_page.create_register_window()

    back_button = ctk.CTkButton(form_frame, text="Back", font=("Helvetica", 14), command=on_back_click)
    back_button.grid(row=15, column=0, columnspan=2, pady=10)

    clinic_register_root.mainloop()

if __name__ == "__main__":
    create_clinic_register_window()

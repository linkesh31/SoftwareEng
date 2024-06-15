import tkinter as tk
import mysql.connector
from tkinter import messagebox, filedialog, ttk

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
    global clinic_register_root
    clinic_register_root = tk.Tk()
    clinic_register_root.title("Clinic Registration")
    width = 600
    height = 800
    clinic_register_root.geometry(f"{width}x{height}")

    top_frame = tk.Frame(clinic_register_root, bg="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)

    title_label = tk.Label(top_frame, text="Call a Doctor", font=("Arial", 24), bg="#ADD8E6", fg="#13126C")
    title_label.pack(pady=10)

    sub_title_label = tk.Label(top_frame, text="Welcome to Registration", font=("Arial", 18), bg="#ADD8E6", fg="#13126C")
    sub_title_label.pack(pady=10)

    form_frame = tk.Frame(top_frame, bg="#ADD8E6")
    form_frame.pack(pady=10)

    # Clinic info section
    clinic_info_label = tk.Label(form_frame, text="Clinic info", font=("Arial", 16), bg="#ADD8E6", fg="black")
    clinic_info_label.grid(row=0, column=0, columnspan=2, pady=1)

    clinic_name_label = tk.Label(form_frame, text="Clinic Name:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    clinic_name_label.grid(row=1, column=0, sticky="e", pady=5)
    clinic_name_entry = tk.Entry(form_frame, font=("Arial", 14))
    clinic_name_entry.grid(row=1, column=1, pady=5)

    clinic_address_label = tk.Label(form_frame, text="Clinic Address:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    clinic_address_label.grid(row=2, column=0, sticky="e", pady=5)
    clinic_address_entry = tk.Entry(form_frame, font=("Arial", 14))
    clinic_address_entry.grid(row=2, column=1, pady=5)

    clinic_license_label = tk.Label(form_frame, text="Clinic License:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    clinic_license_label.grid(row=3, column=0, sticky="e", pady=5)
    clinic_license_button = tk.Button(form_frame, text="Choose File", font=("Arial", 12))
    clinic_license_button.grid(row=3, column=1, pady=5)
    clinic_license_path_label = tk.Label(form_frame, text="", font=("Arial", 12), bg="#ADD8E6", fg="black")
    clinic_license_path_label.grid(row=4, column=0, columnspan=2, pady=5)

    def choose_file():
        path = browse_file()
        clinic_license_path_label.config(text=path)

    clinic_license_button.config(command=choose_file)

    # Clinic admin info section
    clinic_admin_info_label = tk.Label(form_frame, text="Clinic Admin info", font=("Arial", 16), bg="#ADD8E6", fg="black")
    clinic_admin_info_label.grid(row=5, column=0, columnspan=2, pady=5)

    fullname_label = tk.Label(form_frame, text="Fullname:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    fullname_label.grid(row=6, column=0, sticky="e", pady=5)
    fullname_entry = tk.Entry(form_frame, font=("Arial", 14))
    fullname_entry.grid(row=6, column=1, pady=5)

    email_label = tk.Label(form_frame, text="Email:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    email_label.grid(row=7, column=0, sticky="e", pady=5)
    email_entry = tk.Entry(form_frame, font=("Arial", 14))
    email_entry.grid(row=7, column=1, pady=5)

    username_label = tk.Label(form_frame, text="Username:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    username_label.grid(row=8, column=0, sticky="e", pady=5)
    username_entry = tk.Entry(form_frame, font=("Arial", 14))
    username_entry.grid(row=8, column=1, pady=5)

    password_label = tk.Label(form_frame, text="Password:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    password_label.grid(row=9, column=0, sticky="e", pady=5)
    password_entry = tk.Entry(form_frame, font=("Arial", 14), show="*")
    password_entry.grid(row=9, column=1, pady=5)

    confirm_password_label = tk.Label(form_frame, text="Confirm Password:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    confirm_password_label.grid(row=10, column=0, sticky="e", pady=5)
    confirm_password_entry = tk.Entry(form_frame, font=("Arial", 14), show="*")
    confirm_password_entry.grid(row=10, column=1, pady=5)

    phone_number_label = tk.Label(form_frame, text="Phone Number:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    phone_number_label.grid(row=11, column=0, sticky="e", pady=5)
    phone_number_entry = tk.Entry(form_frame, font=("Arial", 14))
    phone_number_entry.grid(row=11, column=1, pady=5)

    admin_address_label = tk.Label(form_frame, text="Admin Address:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    admin_address_label.grid(row=12, column=0, sticky="e", pady=5)
    admin_address_entry = tk.Entry(form_frame, font=("Arial", 14))
    admin_address_entry.grid(row=12, column=1, pady=5)

    date_of_birth_label = tk.Label(form_frame, text="Date of Birth:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    date_of_birth_label.grid(row=13, column=0, sticky="e", pady=5)

    years = [str(year) for year in range(1900, 2025)]
    months = [str(month).zfill(2) for month in range(1, 13)]
    days = [str(day).zfill(2) for day in range(1, 32)]

    year_var = tk.StringVar(form_frame)
    year_var.set(years[0])
    month_var = tk.StringVar(form_frame)
    month_var.set(months[0])
    day_var = tk.StringVar(form_frame)
    day_var.set(days[0])

    year_menu = ttk.Combobox(form_frame, textvariable=year_var, values=years)
    year_menu.grid(row=13, column=1, sticky="w", pady=5)
    year_menu.config(state="readonly")

    month_menu = ttk.Combobox(form_frame, textvariable=month_var, values=months)
    month_menu.grid(row=13, column=1, pady=5)
    month_menu.config(state="readonly")

    day_menu = ttk.Combobox(form_frame, textvariable=day_var, values=days)
    day_menu.grid(row=13, column=1, sticky="e", pady=5)
    day_menu.config(state="readonly")

    def on_register_click():
        clinic_name = clinic_name_entry.get()
        clinic_address = clinic_address_entry.get()
        clinic_license_path = clinic_license_path_label.cget("text")
        admin_fullname = fullname_entry.get()
        admin_username = username_entry.get()
        admin_password = password_entry.get()
        admin_email = email_entry.get()
        admin_phone_number = phone_number_entry.get()
        admin_address = admin_address_entry.get()
        admin_date_of_birth = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"

        if admin_password != confirm_password_entry.get():
            messagebox.showerror("Error", "Passwords do not match!")
            return

        submit_clinic_data(clinic_name, clinic_address, clinic_license_path, admin_fullname, admin_username, admin_password, admin_email, admin_phone_number, admin_date_of_birth, admin_address)

    register_button = tk.Button(form_frame, text="Register", font=("Arial", 14), command=on_register_click)
    register_button.grid(row=14, column=0, columnspan=2, pady=10)

    def on_back_click():
        clinic_register_root.destroy()
        import register_page
        register_page.create_register_window()

    back_button = tk.Button(form_frame, text="Back", font=("Arial", 14), command=on_back_click)
    back_button.grid(row=15, column=0, columnspan=2, pady=10)

    clinic_register_root.mainloop()

if __name__ == "__main__":
    create_clinic_register_window()
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
        messagebox.showinfo("Success", "Clinic registered successfully!")
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
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    return filename

def create_clinic_register_window():
    global clinic_register_root
    clinic_register_root = tk.Tk()
    clinic_register_root.title("Clinic Registration")
    width = 600
    height = 700
    clinic_register_root.geometry(f"{width}x{height}")

    top_frame = tk.Frame(clinic_register_root, bg="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)

    title_label = tk.Label(top_frame, text="Call a Doctor", font=("Arial", 24), bg="#ADD8E6", fg="#13126C")
    title_label.place(relx=0.5, rely=0.05, anchor="center")

    sub_title_label = tk.Label(top_frame, text="Welcome to Registration", font=("Arial", 18), bg="#ADD8E6", fg="#13126C")
    sub_title_label.place(relx=0.5, rely=0.15, anchor="center")

    clinic_info_label = tk.Label(top_frame, text="Clinic info", font=("Arial", 16), bg="#ADD8E6", fg="black")
    clinic_info_label.place(relx=0.1, rely=0.2, anchor="w")

    clinic_name_label = tk.Label(top_frame, text="Clinic Name:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    clinic_name_label.place(relx=0.1, rely=0.25, anchor="w")
    clinic_name_entry = tk.Entry(top_frame, font=("Arial", 14))
    clinic_name_entry.place(relx=0.4, rely=0.25, anchor="w")

    clinic_address_label = tk.Label(top_frame, text="Clinic Address:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    clinic_address_label.place(relx=0.1, rely=0.3, anchor="w")
    clinic_address_entry = tk.Entry(top_frame, font=("Arial", 14))
    clinic_address_entry.place(relx=0.4, rely=0.3, anchor="w")

    clinic_license_label = tk.Label(top_frame, text="Clinic License:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    clinic_license_label.place(relx=0.1, rely=0.35, anchor="w")
    clinic_license_button = tk.Button(top_frame, text="Choose File", font=("Arial", 12), command=lambda: browse_file())
    clinic_license_button.place(relx=0.4, rely=0.35, anchor="w")
    clinic_license_path_label = tk.Label(top_frame, text="", font=("Arial", 12), bg="#ADD8E6", fg="black")
    clinic_license_path_label.place(relx=0.6, rely=0.35, anchor="w")

    def choose_file():
        path = browse_file()
        clinic_license_path_label.config(text=path)

    clinic_license_button.config(command=choose_file)

    clinic_admin_info_label = tk.Label(top_frame, text="Clinic Admin info", font=("Arial", 16), bg="#ADD8E6", fg="black")
    clinic_admin_info_label.place(relx=0.1, rely=0.4, anchor="w")

    fullname_label = tk.Label(top_frame, text="Fullname:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    fullname_label.place(relx=0.1, rely=0.45, anchor="w")
    fullname_entry = tk.Entry(top_frame, font=("Arial", 14))
    fullname_entry.place(relx=0.4, rely=0.45, anchor="w")

    email_label = tk.Label(top_frame, text="Email:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    email_label.place(relx=0.1, rely=0.5, anchor="w")
    email_entry = tk.Entry(top_frame, font=("Arial", 14))
    email_entry.place(relx=0.4, rely=0.5, anchor="w")

    username_label = tk.Label(top_frame, text="Username:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    username_label.place(relx=0.1, rely=0.55, anchor="w")
    username_entry = tk.Entry(top_frame, font=("Arial", 14))
    username_entry.place(relx=0.4, rely=0.55, anchor="w")

    password_label = tk.Label(top_frame, text="Password:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    password_label.place(relx=0.1, rely=0.6, anchor="w")
    password_entry = tk.Entry(top_frame, font=("Arial", 14), show="*")
    password_entry.place(relx=0.4, rely=0.6, anchor="w")

    confirm_password_label = tk.Label(top_frame, text="Confirm Password:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    confirm_password_label.place(relx=0.1, rely=0.65, anchor="w")
    confirm_password_entry = tk.Entry(top_frame, font=("Arial", 14), show="*")
    confirm_password_entry.place(relx=0.4, rely=0.65, anchor="w")

    phone_number_label = tk.Label(top_frame, text="Phone Number:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    phone_number_label.place(relx=0.1, rely=0.7, anchor="w")
    phone_number_entry = tk.Entry(top_frame, font=("Arial", 14))
    phone_number_entry.place(relx=0.4, rely=0.7, anchor="w")

    admin_address_label = tk.Label(top_frame, text="Admin Address:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    admin_address_label.place(relx=0.1, rely=0.75, anchor="w")
    admin_address_entry = tk.Entry(top_frame, font=("Arial", 14))
    admin_address_entry.place(relx=0.4, rely=0.75, anchor="w")

    date_of_birth_label = tk.Label(top_frame, text="Date of Birth:", font=("Arial", 14), bg="#ADD8E6", fg="black")
    date_of_birth_label.place(relx=0.1, rely=0.8, anchor="w")

    years = [str(year) for year in range(1900, 2025)]
    months = [str(month).zfill(2) for month in range(1, 13)]
    days = [str(day).zfill(2) for day in range(1, 32)]

    year_var = tk.StringVar(top_frame)
    year_var.set(years[0])
    month_var = tk.StringVar(top_frame)
    month_var.set(months[0])
    day_var = tk.StringVar(top_frame)
    day_var.set(days[0])

    year_menu = ttk.Combobox(top_frame, textvariable=year_var, values=years)
    year_menu.place(relx=0.4, rely=0.8, anchor="w")
    year_menu.config(state="readonly")

    month_menu = ttk.Combobox(top_frame, textvariable=month_var, values=months)
    month_menu.place(relx=0.55, rely=0.8, anchor="w")
    month_menu.config(state="readonly")

    day_menu = ttk.Combobox(top_frame, textvariable=day_var, values=days)
    day_menu.place(relx=0.7, rely=0.8, anchor="w")
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

    register_button = tk.Button(top_frame, text="Register", font=("Arial", 14), command=on_register_click)
    register_button.place(relx=0.5, rely=0.9, anchor="center")

    def on_back_click():
        clinic_register_root.destroy()
        import register_page
        register_page.create_register_window()

    back_button = tk.Button(top_frame, text="Back", font=("Arial", 14), command=on_back_click)
    back_button.place(relx=0.1, rely=0.9, anchor="center")

    clinic_register_root.mainloop()

if __name__ == "__main__":
    create_clinic_register_window()

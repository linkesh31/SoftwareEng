import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import re
import mysql.connector
from mysql.connector import Error

class PatientRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Call a Doctor")
        self.root.geometry("800x600")
        self.root.configure(bg='lightblue')

        title_label = tk.Label(root, text="Call a Doctor", font=("Helvetica", 24, "bold"), bg='lightblue')
        title_label.pack(pady=10)

        subtitle_label = tk.Label(root, text="Welcome to Registration", font=("Helvetica", 18), bg='lightblue')
        subtitle_label.pack(pady=10)

        self.frame = tk.Frame(root, bg='lightblue')
        self.frame.pack(pady=10, padx=20, expand=True, fill=tk.BOTH)

        self.create_form()

        back_button = tk.Button(root, text="Back", command=self.back, bg='lightblue', font=("Helvetica", 12))
        back_button.pack(side=tk.LEFT, padx=20, pady=10)

        register_button = tk.Button(root, text="Register", command=self.register, bg='lightblue', font=("Helvetica", 12))
        register_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def create_form(self):
        labels = ["Fullname:", "Username:", "Password:", "Confirm Password:", "Gender:", "Address:", "IC:", "Date of Birth:", "Email:", "Tel:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            row = i // 2
            col = i % 2 * 2
            label = tk.Label(self.frame, text=label_text, font=("Helvetica", 14), bg='lightblue')
            label.grid(row=row, column=col, sticky="e", pady=5, padx=5)
            if label_text == "Date of Birth:":
                entry = DateEntry(self.frame, font=("Helvetica", 14), date_pattern='y-mm-dd')
            elif label_text == "Gender:":
                entry = ttk.Combobox(self.frame, font=("Helvetica", 14), values=["Male", "Female", "Rather not to say"])
                entry.current(0)  # Set default value
            else:
                entry = tk.Entry(self.frame, font=("Helvetica", 14), show="*" if "Password" in label_text else "")
                if label_text == "Tel:":
                    entry.config(validate="key", validatecommand=(self.frame.register(self.validate_tel), '%P'))
                if label_text == "IC:":
                    entry.config(validate="key", validatecommand=(self.frame.register(self.validate_ic), '%P'))
            entry.grid(row=row, column=col + 1, pady=5, padx=5, sticky="ew")
            self.entries[label_text] = entry

        for i in range(len(labels) // 2 + 1):
            self.frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.frame.grid_columnconfigure(j, weight=1)

    def validate_tel(self, value_if_allowed):
        """ Validate that the input for the Tel field matches the Malaysian phone number format. """
        pattern = re.compile(r'^\d{0,3}-?\d{0,8}$')
        if pattern.match(value_if_allowed):
            return True
        else:
            return False

    def validate_ic(self, value_if_allowed):
        """ Validate that the input for the IC field matches the Malaysian IC format. """
        pattern = re.compile(r'^\d{0,6}-?\d{0,2}-?\d{0,4}$')
        if pattern.match(value_if_allowed):
            return True
        else:
            return False

    def back(self):
        self.root.destroy()
        import main_page
        main_page.create_login_window()

    def register(self):
        data = {label: entry.get() for label, entry in self.entries.items()}
        missing_data = [label for label, entry in data.items() if not entry]

        if missing_data:
            messagebox.showerror("Error", f"Please fill all the fields: {', '.join(missing_data)}")
            return

        if data["Password:"] != data["Confirm Password:"]:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Save user data to the database
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='calladoctor1234',
                database='calladoctor'
            )
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, email, phone_number, date_of_birth, address, fullname, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (data["Username:"], data["Password:"], data["Email:"], data["Tel:"], data["Date of Birth:"], data["Address:"], data["Fullname:"], 'patient'))
            user_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO patients (user_id, fullname, identification_number, gender)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, data["Fullname:"], data["IC:"], data["Gender:"]))
            connection.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.root.destroy()
            import main_page
            main_page.create_login_window()
        except Error as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def create_patient_register_window():
    root = tk.Tk()
    app = PatientRegisterApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_patient_register_window()
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import re
import mysql.connector
from mysql.connector import Error

class PatientRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Call a Doctor")
        self.root.geometry("800x600")

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        title_label = ctk.CTkLabel(root, text="Call a Doctor", font=("Helvetica", 24, "bold"), text_color="black")
        title_label.pack(pady=10)

        subtitle_label = ctk.CTkLabel(root, text="Welcome to Registration", font=("Helvetica", 18), text_color="black")
        subtitle_label.pack(pady=10)

        self.frame = ctk.CTkFrame(root, fg_color='#D3D3D3')
        self.frame.pack(pady=10, padx=20, expand=True, fill=ctk.BOTH)

        self.create_form()

        self.back_button = ctk.CTkButton(root, text="Back", fg_color='#FF6347', font=("Helvetica", 12), text_color="black", command=self.back)
        self.back_button.pack(side=ctk.LEFT, padx=20, pady=10)

        self.register_button = ctk.CTkButton(root, text="Register", fg_color='#32CD32', font=("Helvetica", 12), text_color="black", command=self.register)
        self.register_button.pack(side=ctk.RIGHT, padx=20, pady=10)

        self.back_button.bind("<Enter>", self.on_enter_back)
        self.back_button.bind("<Leave>", self.on_leave_back)
        self.register_button.bind("<Enter>", self.on_enter_register)
        self.register_button.bind("<Leave>", self.on_leave_register)

    def create_form(self):
        labels = ["Fullname:", "Username:", "Password:", "Confirm Password:", "Gender:", "Address:", "IC:", "Date of Birth:", "Email:", "Tel:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            row = i // 2
            col = i % 2 * 2
            label = ctk.CTkLabel(self.frame, text=label_text, font=("Helvetica", 14), text_color="black")
            label.grid(row=row, column=col, sticky="e", pady=5, padx=5)
            if label_text == "Date of Birth:":
                entry = DateEntry(self.frame, font=("Helvetica", 14), date_pattern='y-mm-dd')
            elif label_text == "Gender:":
                entry = ctk.CTkComboBox(self.frame, values=["Male", "Female"], font=("Helvetica", 14), fg_color="white", text_color="black")
                entry.set("Male")  # Set default value
            else:
                entry = ctk.CTkEntry(self.frame, font=("Helvetica", 14), fg_color="white", text_color="black", show="*" if "Password" in label_text else "")
                if label_text == "Tel:":
                    entry.configure(validate="key", validatecommand=(self.frame.register(self.validate_tel), '%P'))
                if label_text == "IC:":
                    entry.configure(validate="key", validatecommand=(self.frame.register(self.validate_ic), '%P'))
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

    def on_enter_back(self, event):
        self.back_button.configure(fg_color='#FF4500')

    def on_leave_back(self, event):
        self.back_button.configure(fg_color='#FF6347')

    def on_enter_register(self, event):
        self.register_button.configure(fg_color='#228B22')

    def on_leave_register(self, event):
        self.register_button.configure(fg_color='#32CD32')

def create_patient_register_window():
    root = ctk.CTk()
    root.configure(bg='lightblue')  # Set the background color for the CTk window
    app = PatientRegisterApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_patient_register_window()
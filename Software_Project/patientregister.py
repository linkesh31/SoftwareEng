import tkinter as tk
from tkinter import messagebox

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
        self.frame.pack(pady=10, padx=20)

        self.create_form()

        back_button = tk.Button(root, text="Back", command=self.back, bg='lightblue', font=("Helvetica", 12))
        back_button.pack(side=tk.LEFT, padx=20, pady=10)

        register_button = tk.Button(root, text="Register", command=self.register, bg='lightblue', font=("Helvetica", 12))
        register_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def create_form(self):
        labels = ["Fullname:", "Username:", "Password:", "Confirm Password:", "Gender:", "Address:", "IC:", "Date of Birth", "Email:", "Tel:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            row = i // 2
            col = i % 2 * 2
            label = tk.Label(self.frame, text=label_text, font=("Helvetica", 14), bg='lightblue')
            label.grid(row=row, column=col, sticky="e", pady=5)
            entry = tk.Entry(self.frame, font=("Helvetica", 14), show="*" if "Password" in label_text else "")
            entry.grid(row=row, column=col + 1, pady=5, padx=5)
            self.entries[label_text] = entry

    def back(self):
        self.root.destroy()
        import register_page
        register_page.create_register_window()

    def register(self):
        data = {label: entry.get() for label, entry in self.entries.items()}
        missing_data = [label for label, entry in data.items() if not entry]

        if missing_data:
            messagebox.showerror("Error", f"Please fill all the fields: {', '.join(missing_data)}")
            return

        # Here, you can add code to handle the registration logic, such as storing the data in the database.
        messagebox.showinfo("Success", "Registration successful!")

def create_patient_register_window():
    root = tk.Tk()
    app = PatientRegisterApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_patient_register_window()

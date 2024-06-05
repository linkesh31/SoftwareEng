import tkinter as tk
from tkinter import filedialog, messagebox

class CallADoctorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Call a Doctor")
        self.root.geometry("500x400")
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
        tk.Label(self.frame, text="Clinic Name:", font=("Helvetica", 14), bg='lightblue').grid(row=0, column=0, sticky="e", pady=5)
        self.clinic_name_entry = tk.Entry(self.frame, font=("Helvetica", 14))
        self.clinic_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.frame, text="Address:", font=("Helvetica", 14), bg='lightblue').grid(row=1, column=0, sticky="e", pady=5)
        self.address_entry = tk.Entry(self.frame, font=("Helvetica", 14))
        self.address_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.frame, text="Clinic License:", font=("Helvetica", 14), bg='lightblue').grid(row=2, column=0, sticky="e", pady=5)
        self.file_label = tk.Label(self.frame, text="No file chosen", font=("Helvetica", 12), bg='lightblue')
        self.file_label.grid(row=2, column=1, pady=5, sticky="w")
        self.choose_file_button = tk.Button(self.frame, text="Choose File", command=self.choose_file, bg='lightblue', font=("Helvetica", 12))
        self.choose_file_button.grid(row=2, column=1, pady=5, sticky="e")

    def choose_file(self):
        self.filepath = filedialog.askopenfilename()
        self.file_label.config(text=self.filepath.split('/')[-1])

    def back(self):
        self.root.destroy()
        import register_page
        register_page.create_register_window()

    def register(self):
        clinic_name = self.clinic_name_entry.get()
        address = self.address_entry.get()
        license_file = getattr(self, 'filepath', None)

        if not clinic_name or not address or not license_file:
            messagebox.showerror("Error", "Please fill all the fields and choose a file.")
            return

        # Here, you can add code to handle the registration logic, such as storing the data in the database.
        messagebox.showinfo("Success", "Registration successful!")

def create_clinic_register_window():
    root = tk.Tk()
    app = CallADoctorApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_clinic_register_window()

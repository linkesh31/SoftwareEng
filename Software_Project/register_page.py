import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def create_rounded_image(image_path, size, corner_radius):
    image = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), corner_radius, fill=255)
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

def create_rounded_button_image(image_path, size, corner_radius):
    return create_rounded_image(image_path, size, corner_radius)

def doctor_button_clicked():
    print("Doctor button clicked")

def patient_button_clicked():
    print("Patient button clicked")

def clinic_button_clicked():
    print("Clinic button clicked")

def open_login_page():
    register_root.destroy()
    import main_page
    main_page.create_login_window()

def create_register_window():
    global register_root
    register_root = tk.Tk()
    register_root.title("Register")
    width = 1480
    height = 750
    register_root.geometry(f"{width}x{height}")

    top_frame = tk.Frame(register_root, bg="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)

    image_path = "C:\\Users\\linke\\OneDrive\\Documents\\GitHub\\SoftwareEng\\Software_Project\\SoftwareLogo.png"
    logo_image = create_rounded_image(image_path, (150, 150), 30)
    photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(top_frame, image=photo, bg="#ADD8E6")
    logo_label.image = photo
    logo_label.place(relx=1.0, rely=0.0, anchor="ne")

    login_text = tk.Label(top_frame, text="Registration", font=("Arial", 14), bg="#ADD8E6", fg="black")
    login_text.place(relx=0.01, rely=0.01, anchor="nw")

    welcome_label = tk.Label(top_frame, text="Welcome to Registration", font=("Arial", 24), bg="#ADD8E6", fg="white")
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")

    login_type_label = tk.Label(top_frame, text="Are you?", font=("Arial", 24), bg="#ADD8E6", fg="white")
    login_type_label.place(relx=0.5, rely=0.25, anchor="center")

    button_size = (200, 200)
    corner_radius = 20

    doctor_image_path = "C:\\Users\\linke\\OneDrive\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Doctor.png"
    doctor_image = create_rounded_button_image(doctor_image_path, button_size, corner_radius)
    doctor_photo = ImageTk.PhotoImage(doctor_image)

    patient_image_path = "C:\\Users\\linke\\OneDrive\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Patient.png"
    patient_image = create_rounded_button_image(patient_image_path, button_size, corner_radius)
    patient_photo = ImageTk.PhotoImage(patient_image)

    clinic_image_path = "C:\\Users\\linke\\OneDrive\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Clinic.png"
    clinic_image = create_rounded_button_image(clinic_image_path, button_size, corner_radius)
    clinic_photo = ImageTk.PhotoImage(clinic_image)

    doctor_button = tk.Button(top_frame, image=doctor_photo, command=doctor_button_clicked, borderwidth=0, bg="#ADD8E6")
    doctor_button.place(relx=0.3, rely=0.45, anchor="center")

    patient_button = tk.Button(top_frame, image=patient_photo, command=patient_button_clicked, borderwidth=0, bg="#ADD8E6")
    patient_button.place(relx=0.5, rely=0.45, anchor="center")

    clinic_button = tk.Button(top_frame, image=clinic_photo, command=clinic_button_clicked, borderwidth=0, bg="#ADD8E6")
    clinic_button.place(relx=0.7, rely=0.45, anchor="center")

    doctor_label = tk.Label(top_frame, text="Doctor", font=("Arial", 14), bg="#ADD8E6", fg="black")
    doctor_label.place(relx=0.3, rely=0.60, anchor="center")

    patient_label = tk.Label(top_frame, text="Patient", font=("Arial", 14), bg="#ADD8E6", fg="black")
    patient_label.place(relx=0.5, rely=0.60, anchor="center")

    clinic_label = tk.Label(top_frame, text="Clinic", font=("Arial", 14), bg="#ADD8E6", fg="black")
    clinic_label.place(relx=0.7, rely=0.60, anchor="center")

    login_frame = tk.Frame(top_frame, bg="#ADD8E6")
    login_frame.place(relx=0.99, rely=0.99, anchor="se")

    login_label_text = tk.Label(login_frame, text="Already have an account, ", font=("Arial", 12), bg="#ADD8E6", fg="white")
    login_label_text.pack(side="left")

    click_here_login_label = tk.Label(login_frame, text="click here", font=("Arial", 12), bg="#ADD8E6", fg="#0000EE", cursor="hand2")
    click_here_login_label.pack(side="left")
    click_here_login_label.bind("<Button-1>", lambda event: open_login_page())

    register_root.mainloop()

if __name__ == "__main__":
    create_register_window()

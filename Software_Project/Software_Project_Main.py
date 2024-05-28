import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Function to create an image with rounded corners
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
    pass

def patient_button_clicked():
    pass

def clinic_button_clicked():
    pass


def admin_login_clicked(event):
    print("Admin login clicked")  # Placeholder action

def login_clicked(event):
    root.destroy()
    open_register_page()

def open_register_page():
    with open("C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Software_Project_Register_Page.py") as file:
        exec(file.read())

def create_login_window():
    global root
    root = tk.Tk()
    root.title("Login")
    width = 1480
    height = 750
    root.geometry(f"{width}x{height}")

    top_frame = tk.Frame(root, bg="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)

    image_path = "C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\SoftwareLogo.png"
    logo_image = create_rounded_image(image_path, (150, 150), 30)
    photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(top_frame, image=photo, bg="#ADD8E6")
    logo_label.image = photo
    logo_label.place(relx=1.0, rely=0.0, anchor="ne")

    login_text = tk.Label(top_frame, text="Login", font=("Arial", 14), bg="#ADD8E6", fg="black")
    login_text.place(relx=0.01, rely=0.01, anchor="nw")

    welcome_label = tk.Label(top_frame, text="Welcome to Login", font=("Arial", 24), bg="#ADD8E6", fg="white")
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")

    login_type_label = tk.Label(top_frame, text="Are you?", font=("Arial", 24), bg="#ADD8E6", fg="white")
    login_type_label.place(relx=0.5, rely=0.25, anchor="center")

    button_size = (200, 200)
    corner_radius = 20

    doctor_image_path = "C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Doctor.png"
    doctor_image = create_rounded_button_image(doctor_image_path, button_size, corner_radius)
    doctor_photo = ImageTk.PhotoImage(doctor_image)

    patient_image_path = "C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Patient.png"
    patient_image = create_rounded_button_image(patient_image_path, button_size, corner_radius)
    patient_photo = ImageTk.PhotoImage(patient_image)

    doctor_button = tk.Button(top_frame, image=doctor_photo, command=doctor_button_clicked, borderwidth=0, bg="#ADD8E6")
    doctor_button.place(relx=0.4, rely=0.45, anchor="center")

    patient_button = tk.Button(top_frame, image=patient_photo, command=patient_button_clicked, borderwidth=0, bg="#ADD8E6")
    patient_button.place(relx=0.6, rely=0.45, anchor="center")

    doctor_label = tk.Label(top_frame, text="Doctor", font=("Arial", 14), bg="#ADD8E6", fg="black")
    doctor_label.place(relx=0.4, rely=0.60, anchor="center")

    patient_label = tk.Label(top_frame, text="Patient", font=("Arial", 14), bg="#ADD8E6", fg="black")
    patient_label.place(relx=0.6, rely=0.60, anchor="center")

    admin_frame = tk.Frame(top_frame, bg="#ADD8E6")
    admin_frame.place(relx=0.01, rely=0.99, anchor="sw")

    admin_label = tk.Label(admin_frame, text="If you're the admin,", font=("Arial", 12), bg="#ADD8E6", fg="white")
    admin_label.pack(side="left")

    click_here_label = tk.Label(admin_frame, text="Click here", font=("Arial", 12), bg="#ADD8E6", fg="#0000EE", cursor="hand2")
    click_here_label.pack(side="left")
    click_here_label.bind("<Button-1>", admin_login_clicked)

    login_frame = tk.Frame(top_frame, bg="#ADD8E6")
    login_frame.place(relx=0.99, rely=0.99, anchor="se")

    login_label_text = tk.Label(login_frame, text="Don’t have an account, ", font=("Arial", 12), bg="#ADD8E6", fg="white")
    login_label_text.pack(side="left")

    click_here_login_label = tk.Label(login_frame, text="click here", font=("Arial", 12), bg="#ADD8E6", fg="#0000EE", cursor="hand2")
    click_here_login_label.pack(side="left")
    click_here_login_label.bind("<Button-1>", login_clicked)

    root.mainloop()

create_login_window()

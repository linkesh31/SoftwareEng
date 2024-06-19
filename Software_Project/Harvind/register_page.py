import customtkinter as ctk
from PIL import Image, ImageDraw
import mysql.connector

# Create rounded image function
def create_rounded_image(image_path, size, corner_radius):
    image = Image.open(image_path).resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), corner_radius, fill=255)
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

# Create rounded button image function
def create_rounded_button_image(image_path, size, corner_radius):
    return create_rounded_image(image_path, size, corner_radius)

# Button click events
def patient_button_clicked():
    register_root.destroy()
    import patientregister
    patientregister.create_patient_register_window()

def clinic_button_clicked():
    register_root.destroy()
    import clinicregister
    clinicregister.create_clinic_register_window()

def open_login_page():
    register_root.destroy()
    import main_page
    main_page.create_login_window()

# Create register window function
def create_register_window():
    global register_root
    ctk.set_appearance_mode("light")  # Modes: "light", "dark", "system"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    register_root = ctk.CTk()
    register_root.title("Register")
    width = 600
    height = 500
    register_root.geometry(f"{width}x{height}")

    top_frame = ctk.CTkFrame(register_root, fg_color="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)

    image_path = "C://Users//user//Documents//GitHub//SoftwareEng//Software_Project//Harvind//Images//SoftwareLogo.png"
    logo_image = create_rounded_image(image_path, (100, 100), 20)
    logo_photo = ctk.CTkImage(light_image=logo_image, size=(100, 100))
    logo_label = ctk.CTkLabel(top_frame, image=logo_photo, fg_color="#ADD8E6", text="")
    logo_label.place(relx=0.99, rely=0.01, anchor="ne")

    welcome_label = ctk.CTkLabel(top_frame, text="Welcome to Registration", font=("Times New Roman", 28), fg_color="#ADD8E6", text_color="#13126C")
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")

    button_size = (120, 120)
    corner_radius = 15

    patient_image_path = "C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Harvind\\Images\\Patient.png"
    patient_image = create_rounded_button_image(patient_image_path, button_size, corner_radius)
    patient_photo = ctk.CTkImage(light_image=patient_image, size=button_size)

    clinic_image_path = "C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Harvind\\Images\\Clinic.png"
    clinic_image = create_rounded_button_image(clinic_image_path, button_size, corner_radius)
    clinic_photo = ctk.CTkImage(light_image=clinic_image, size=button_size)

    patient_button = ctk.CTkButton(top_frame, image=patient_photo, command=patient_button_clicked, fg_color="#ADD8E6", hover_color="#5A9BD4", text="")
    patient_button.place(relx=0.35, rely=0.45, anchor="center")

    clinic_button = ctk.CTkButton(top_frame, image=clinic_photo, command=clinic_button_clicked, fg_color="#ADD8E6", hover_color="#5A9BD4", text="")
    clinic_button.place(relx=0.65, rely=0.45, anchor="center")

    patient_label = ctk.CTkLabel(top_frame, text="Patient", font=("Arial", 16), fg_color="#ADD8E6", text_color="black")
    patient_label.place(relx=0.35, rely=0.60, anchor="center")

    clinic_label = ctk.CTkLabel(top_frame, text="Clinic", font=("Arial", 16), fg_color="#ADD8E6", text_color="black")
    clinic_label.place(relx=0.65, rely=0.60, anchor="center")

    login_frame = ctk.CTkFrame(top_frame, fg_color="#ADD8E6")
    login_frame.place(relx=0.99, rely=0.99, anchor="se")

    login_label_text = ctk.CTkLabel(login_frame, text="Already have an account, ", font=("Arial", 16), fg_color="#ADD8E6", text_color="black")
    login_label_text.pack(side="left")

    click_here_login_label = ctk.CTkLabel(login_frame, text="click here", font=("Arial", 16), fg_color="#ADD8E6", text_color="#0000EE", cursor="hand2")
    click_here_login_label.pack(side="left")
    click_here_login_label.bind("<Button-1>", lambda event: open_login_page())

    register_root.mainloop()

if __name__ == "__main__":
    create_register_window()

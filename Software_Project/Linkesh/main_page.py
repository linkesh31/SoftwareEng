import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import mysql.connector
from mysql.connector import Error
import subprocess

def create_rounded_image(image_path, size, corner_radius):
    image = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, size[0], size[1]], corner_radius, fill=255)
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

def call_doctor_button_clicked():
    print("Call a Doctor button clicked")

def open_register_page():
    login_root.destroy()
    import register_page
    register_page.create_register_window()

def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.insert(0, '')
        entry.config(fg='black')
        if entry == password_entry:
            entry.config(show='*')

def on_focusout(event, entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')
        if entry == password_entry:
            entry.config(show='')

def authenticate_user(username, password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, role, fullname FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        if result:
            user_id, role, fullname = result
            if role == 'doctor':
                cursor.execute("SELECT doctor_id FROM doctors WHERE user_id=%s", (user_id,))
                doctor_result = cursor.fetchone()
                doctor_id = doctor_result[0] if doctor_result else None
                connection.close()
                return role, doctor_id, fullname
            elif role == 'clinic_admin':
                cursor.execute("SELECT clinic_id FROM admin_clinics WHERE admin_id=%s", (user_id,))
                clinic_result = cursor.fetchone()
                clinic_id = clinic_result[0] if clinic_result else None
                connection.close()
                return role, clinic_id, fullname
            else:
                connection.close()
                return role, None, fullname
        else:
            connection.close()
            return None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def login():
    username = username_entry.get()
    password = password_entry.get()
    result = authenticate_user(username, password)
    print(f"Login result: {result}")  # Debug print statement
    if result:
        role, clinic_or_doctor_id, fullname = result
        if role == 'doctor' and clinic_or_doctor_id is None:
            messagebox.showerror("Login Failed", "Doctor ID not found")
            return
        login_root.destroy()
        if role == 'admin':
            subprocess.run(['python', 'adminhome.py', fullname])
        elif role == 'clinic_admin':
            subprocess.run(['python', 'adminclinichome.py', str(clinic_or_doctor_id), fullname])
        elif role == 'doctor':
            subprocess.run(['python', 'doctorhome.py', str(clinic_or_doctor_id)])
        elif role == 'patient':
            subprocess.run(['python', 'patienthome.py', fullname])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def create_login_window():
    global login_root, password_entry, username_entry
    login_root = tk.Tk()
    login_root.title("Login")
    width = 1480
    height = 750
    login_root.geometry(f"{width}x{height}")

    top_frame = tk.Frame(login_root, bg="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)

    logo_path = "C:\\Users\\linke\\OneDrive\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Linkesh\\Images\\SoftwareLogo.png"
    logo_image = create_rounded_image(logo_path, (150, 150), 30)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(top_frame, image=logo_photo, bg="#ADD8E6")
    logo_label.image = logo_photo
    logo_label.place(relx=1.0, rely=0.0, anchor="ne")

    welcome_label = tk.Label(top_frame, text="Welcome to Login", font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#000080")
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")

    user_icon_path = "C:\\Users\\linke\\OneDrive\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Linkesh\\Images\\Patientnobg.png"
    user_icon = create_rounded_image(user_icon_path, (150, 150), 20)
    user_photo = ImageTk.PhotoImage(user_icon)
    user_icon_label = tk.Label(top_frame, image=user_photo, bg="#ADD8E6")
    user_icon_label.image = user_photo
    user_icon_label.place(relx=0.5, rely=0.35, anchor="center")

    default_username = "Username"
    default_password = "Password"

    username_entry = tk.Entry(top_frame, font=("Arial", 16), fg='grey')
    username_entry.insert(0, default_username)
    username_entry.bind('<FocusIn>', lambda event: on_entry_click(event, username_entry, default_username))
    username_entry.bind('<FocusOut>', lambda event: on_focusout(event, username_entry, default_username))
    username_entry.place(relx=0.5, rely=0.5, anchor="center", width=300, height=30)

    password_entry = tk.Entry(top_frame, font=("Arial", 16), fg='grey', show='')
    password_entry.insert(0, default_password)
    password_entry.bind('<FocusIn>', lambda event: on_entry_click(event, password_entry, default_password))
    password_entry.bind('<FocusOut>', lambda event: on_focusout(event, password_entry, default_password))
    password_entry.place(relx=0.5, rely=0.55, anchor="center", width=300, height=30)

    login_button = tk.Button(top_frame, text="Login", font=("Arial", 16), command=login)
    login_button.place(relx=0.5, rely=0.6, anchor="center")

    login_frame = tk.Frame(top_frame, bg="#ADD8E6")
    login_frame.place(relx=0.99, rely=0.99, anchor="se")

    login_label_text = tk.Label(login_frame, text="Don't have an account? ", font=("Arial", 12), bg="#ADD8E6", fg="white")
    login_label_text.pack(side="left")

    click_here_register_label = tk.Label(login_frame, text="Click here", font=("Arial", 12), bg="#ADD8E6", fg="#0000EE", cursor="hand2")
    click_here_register_label.pack(side="left")
    click_here_register_label.bind("<Button-1>", lambda event: open_register_page())

    login_root.mainloop()

if __name__ == "__main__":
    create_login_window()
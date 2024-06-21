import customtkinter as ctk  # Import customtkinter for creating custom UI elements
from tkinter import messagebox  # Import messagebox for showing dialog boxes
from PIL import Image, ImageDraw  # Import PIL for image processing
import mysql.connector  # Import mysql.connector for database connectivity
from mysql.connector import Error  # Import Error for handling database errors
import subprocess  # Import subprocess for running external scripts

# Function to create a rounded image
def create_rounded_image(image_path, size, corner_radius):
    # Open and resize the image
    image = Image.open(image_path).resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    # Create a mask for rounded corners
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), corner_radius, fill=255)
    # Create a new image with rounded corners
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

# Function to open the register page
def open_register_page():
    login_root.destroy()  # Close the login window
    import register_page  # Import the register page script
    register_page.create_register_window()  # Open the register window

# Event handler for entry click
def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:  # Check if the entry contains default text
        entry.delete(0, "end")  # Clear the entry
        entry.insert(0, '')  # Insert an empty string
        entry.configure(text_color='black')  # Change text color to black
        if entry == password_entry:
            entry.configure(show='*')  # Mask the password entry

# Event handler for focus out
def on_focusout(event, entry, default_text):
    if entry.get() == '':  # Check if the entry is empty
        entry.insert(0, default_text)  # Insert the default text
        entry.configure(text_color='grey')  # Change text color to grey
        if entry == password_entry:
            entry.configure(show='')  # Unmask the password entry

# Function to authenticate the user
def authenticate_user(username, password):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='calladoctor1234',
            database='calladoctor'
        )
        cursor = connection.cursor()  # Create a cursor object
        # Execute the query to check user credentials
        cursor.execute("SELECT user_id, role, fullname FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()  # Fetch the result
        if result:
            user_id, role, fullname = result
            if role == 'doctor':
                # Check if the user is a doctor
                cursor.execute("SELECT doctor_id FROM doctors WHERE user_id=%s", (user_id,))
                doctor_result = cursor.fetchone()
                doctor_id = doctor_result[0] if doctor_result else None
                connection.close()
                return role, doctor_id, fullname
            elif role == 'clinic_admin':
                # Check if the user is a clinic admin
                cursor.execute("SELECT c.clinic_id, c.is_approved FROM admin_clinics ac JOIN clinics c ON ac.clinic_id = c.clinic_id WHERE ac.admin_id=%s", (user_id,))
                clinic_result = cursor.fetchone()
                clinic_id, is_approved = clinic_result if clinic_result else (None, None)
                if is_approved == 0:
                    connection.close()
                    return None
                connection.close()
                return role, clinic_id, fullname
            elif role == 'patient':
                # Check if the user is a patient
                cursor.execute("SELECT patient_id FROM patients WHERE user_id=%s", (user_id,))
                patient_result = cursor.fetchone()
                patient_id = patient_result[0] if patient_result else None
                connection.close()
                return role, patient_id, fullname
            else:
                connection.close()
                return role, None, fullname
        else:
            connection.close()
            return None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

# Function to handle login
def login():
    username = username_entry.get()  # Get the username
    password = password_entry.get()  # Get the password
    if username == "Username" or password == "Password":
        messagebox.showerror("Login Failed", "Please fill out all fields")
        return
    result = authenticate_user(username, password)  # Authenticate the user
    print(f"Login result: {result}")  # Debug print statement
    if result:
        role, id, fullname = result
        if role == 'doctor' and id is None:
            messagebox.showerror("Login Failed", "Doctor ID not found")
            return
        login_root.destroy()  # Close the login window
        if role == 'admin':
            subprocess.run(['python', 'adminhome.py', fullname])
        elif role == 'clinic_admin':
            subprocess.run(['python', 'adminclinichome.py', str(id), fullname])
        elif role == 'doctor':
            subprocess.run(['python', 'doctorhome.py', str(id)])
        elif role == 'patient':
            subprocess.run(['python', 'patienthome.py', str(id), fullname])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to open the forgot password page
def open_forgot_password_page():
    login_root.destroy()  # Close the login window
    subprocess.run(['python', 'forgot_password.py'])  # Run the forgot password script

# Function to create the login window
def create_login_window():
    global login_root, password_entry, username_entry
    ctk.set_appearance_mode("light")  # Set the appearance mode
    ctk.set_default_color_theme("blue")  # Set the default color theme

    login_root = ctk.CTk()  # Create the main window
    login_root.title("Login")  # Set the window title
    width = 880
    height = 650
    login_root.geometry(f"{width}x{height}")  # Set the window size

    top_frame = ctk.CTkFrame(login_root, fg_color="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)  # Create and pack the top frame

    logo_path = "C://Users//linke//OneDrive//Documents//GitHub//SoftwareEng//Software_Project//Linkesh//Images//SoftwareLogo.png"
    logo_image = create_rounded_image(logo_path, (150, 150), 30)  # Create a rounded logo image
    logo_photo = ctk.CTkImage(light_image=logo_image, size=(150, 150))
    logo_label = ctk.CTkLabel(top_frame, image=logo_photo, fg_color="#ADD8E6", text="")
    logo_label.place(x=width-10, y=10, anchor="ne")  # Place the logo image

    welcome_label = ctk.CTkLabel(top_frame, text="Welcome to Login", font=("Arial", 24, "bold"), fg_color="#ADD8E6", text_color="#000080")
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")  # Place the welcome label

    user_icon_path = "C://Users//linke//OneDrive//Documents//GitHub//SoftwareEng//Software_Project//Linkesh//Images//Patientnobg.png"
    user_icon = create_rounded_image(user_icon_path, (150, 150), 20)  # Create a rounded user icon
    user_photo = ctk.CTkImage(light_image=user_icon, size=(150, 150))
    user_icon_label = ctk.CTkLabel(top_frame, image=user_photo, fg_color="#ADD8E6", text="")
    user_icon_label.place(relx=0.5, rely=0.35, anchor="center")  # Place the user icon

    default_username = "Username"
    default_password = "Password"

    username_entry = ctk.CTkEntry(top_frame, font=("Arial", 16), fg_color="white", text_color='grey', width=300, height=30)
    username_entry.insert(0, default_username)
    username_entry.bind('<FocusIn>', lambda event: on_entry_click(event, username_entry, default_username))
    username_entry.bind('<FocusOut>', lambda event: on_focusout(event, username_entry, default_username))
    username_entry.place(relx=0.5, rely=0.5, anchor="center")  # Create and place the username entry

    password_entry = ctk.CTkEntry(top_frame, font=("Arial", 16), fg_color="white", text_color='grey', show='*', width=300, height=30)
    password_entry.insert(0, default_password)
    password_entry.bind('<FocusIn>', lambda event: on_entry_click(event, password_entry, default_password))
    password_entry.bind('<FocusOut>', lambda event: on_focusout(event, password_entry, default_password))
    password_entry.place(relx=0.5, rely=0.55, anchor="center")  # Create and place the password entry

    login_button = ctk.CTkButton(top_frame, text="Login", font=("Arial", 16), command=login, fg_color="#4682B4", hover_color="#5A9BD4", text_color="white")
    login_button.place(relx=0.5, rely=0.6, anchor="center")  # Create and place the login button

    forgot_password_label = ctk.CTkLabel(top_frame, text="Forgot Password?", font=("Arial", 12), fg_color="#ADD8E6", text_color="#0000EE", cursor="hand2")
    forgot_password_label.place(relx=0.5, rely=0.65, anchor="center")
    forgot_password_label.bind("<Button-1>", lambda event: open_forgot_password_page())  # Create and place the forgot password label

    login_frame = ctk.CTkFrame(top_frame, fg_color="#ADD8E6")
    login_frame.place(relx=0.99, rely=0.99, anchor="se")  # Create and place the login frame

    login_label_text = ctk.CTkLabel(login_frame, text="Don't have an account? ", font=("Arial", 16), fg_color="#ADD8E6", text_color="black")
    login_label_text.pack(side="left")  # Create and place the login label text

    click_here_register_label = ctk.CTkLabel(login_frame, text="Click here", font=("Arial", 16), fg_color="#ADD8E6", text_color="#0000EE", cursor="hand2")
    click_here_register_label.pack(side="left")
    click_here_register_label.bind("<Button-1>", lambda event: open_register_page())  # Create and place the register label

    login_root.mainloop()  # Start the main loop

if __name__ == "__main__":
    create_login_window()  # Call the function to create the login window

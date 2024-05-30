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

def call_doctor_button_clicked():
    print("Call a Doctor button clicked")

def open_register_page():
    login_root.destroy()
    import register_page
    register_page.create_register_window()
    # Add code to open register page

def on_entry_click(event, entry, default_text):
    """Function that gets called when entry is clicked"""
    if entry.get() == default_text:
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')

def on_focusout(event, entry, default_text):
    """Function that gets called when entry loses focus"""
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')

def create_login_window():
    global login_root
    login_root = tk.Tk()
    login_root.title("Login")
    width = 1480
    height = 750
    login_root.geometry(f"{width}x{height}")

    top_frame = tk.Frame(login_root, bg="#ADD8E6", width=width, height=height)
    top_frame.pack(fill="both", expand=True)

    # Create and place the logo at the top right
    logo_path = "C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\SoftwareLogo.png"
    logo_image = create_rounded_image(logo_path, (150, 150), 30)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(top_frame, image=logo_photo, bg="#ADD8E6")
    logo_label.image = logo_photo
    logo_label.place(relx=1.0, rely=0.0, anchor="ne")

    # Create and place the "Welcome to Login" message
    welcome_label = tk.Label(top_frame, text="Welcome to Login", font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#000080")
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")

    # Create and place the user icon
    user_icon_path = "C:\\Users\\user\\Documents\\GitHub\\SoftwareEng\\Software_Project\\Patientnobg.png"
    user_icon = create_rounded_image(user_icon_path, (150, 150), 20)  # Adjusted size
    user_photo = ImageTk.PhotoImage(user_icon)
    user_icon_label = tk.Label(top_frame, image=user_photo, bg="#ADD8E6")
    user_icon_label.image = user_photo
    user_icon_label.place(relx=0.5, rely=0.35, anchor="center")

    # Create and place the username and password fields with placeholder text
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

    # Create and place the "Don't have an account?" message
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
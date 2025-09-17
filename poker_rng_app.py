import customtkinter as ctk
import random
import ctypes
from ctypes import windll

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# App setup
app = ctk.CTk()
app.overrideredirect(True)
app.wm_attributes("-topmost", True)
app.wm_attributes("-transparentcolor", "white")  # Everything white becomes invisible

# Position: middle right
win_width = 160
win_height = 120
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = screen_width - win_width - 50
y = int((screen_height - win_height) / 6)
app.geometry(f"{win_width}x{win_height}+{x}+{y}")

# Rounded corners (Windows only)
HWND = windll.user32.GetParent(app.winfo_id())
windll.dwmapi.DwmSetWindowAttribute(HWND, 2, ctypes.byref(ctypes.c_int(1)), 4)

# Generate number
def generate(event=None):
    number = random.randint(1, 100)
    display.configure(text=str(number))
    if number <= 25:
        display.configure(text_color="black")
    elif number <= 50:
        display.configure(text_color="red")
    elif number <= 75:
        display.configure(text_color="blue")
    else:
        display.configure(text_color="green")


# Close the app
def close_app():
    app.destroy()

# Drag logic
def start_move(event):
    app._drag_start_x = event.x
    app._drag_start_y = event.y

def do_move(event):
    x = app.winfo_pointerx() - app._drag_start_x
    y = app.winfo_pointery() - app._drag_start_y
    app.geometry(f"+{x}+{y}")

# Transparent background container
transparent_root = ctk.CTkFrame(app, fg_color="white", corner_radius=0)
transparent_root.pack(fill="both", expand=True)

# Visible floating frame (off-white)
floating_frame = ctk.CTkFrame(
    master=transparent_root,
    fg_color="#fefefe",
    corner_radius=20,
    width=150,
    height=90
)
floating_frame.place(relx=0.5, rely=0.5, anchor="center")

# Number display button
display = ctk.CTkButton(
    master=floating_frame,
    text="-",
    font=("Helvetica", 54, "bold"),
    fg_color="#fefefe",
    text_color="black",
    corner_radius=15,
    hover=False,
    width=70,
    height=50,
    command=generate
)
display.place(relx=0.5, rely=0.6, anchor="center")

# Close "X" button
close_btn = ctk.CTkButton(
    master=floating_frame,
    text="✕",
    width=20,
    height=20,
    font=("Helvetica", 12),
    fg_color="#fefefe",
    text_color="gray",
    hover_color="#ddd",
    corner_radius=10,
    command=close_app
)
close_btn.place(relx=0.95, rely=0.05, anchor="ne")

# ✅ Bind drag to the visible frame
floating_frame.bind("<Button-1>", start_move)
floating_frame.bind("<B1-Motion>", do_move)

# Bind generate to the number (so clicking it doesn’t start drag)
display.bind("<Button-1>", generate)

# Escape closes the app
app.bind("<Escape>", lambda e: app.destroy())

# Launch it
app.mainloop()

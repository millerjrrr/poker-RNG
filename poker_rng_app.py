import customtkinter as ctk
import random
import ctypes
from ctypes import windll
from PIL import Image, ImageTk
import sys
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")





def resource_path(relative_path):
    """ Get the absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller stores files in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_rng_window(offset_x=None, offset_y=None):
    win = ctk.CTkToplevel()
    win.overrideredirect(True)
    win.wm_attributes("-topmost", True)

   # Window size
    win_width, win_height = 100, 40
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Center position if no offset provided
    if offset_x is None:
        x = (screen_width - win_width) // 2
    else:
        x = offset_x

    if offset_y is None:
        y = (screen_height - win_height) // 2
    else:
        y = offset_y

    win.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # Rounded corners (Windows only)
    HWND = windll.user32.GetParent(win.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(HWND, 2, ctypes.byref(ctypes.c_int(1)), 4)

    # Drag logic (anywhere)
    def start_move(event):
        win._drag_start_x = event.x
        win._drag_start_y = event.y

    def do_move(event):
        x = win.winfo_pointerx() - win._drag_start_x
        y = win.winfo_pointery() - win._drag_start_y
        win.geometry(f"+{x}+{y}")

    win.bind("<Button-1>", start_move)
    win.bind("<B1-Motion>", do_move)

    # Generate number
    def generate():
        number = random.randint(0, 99)
        display.configure(text=str(number))
        if number < 25:
            display.configure(text_color="black")
        elif number < 50:
            display.configure(text_color="red")
        elif number < 75:
            display.configure(text_color="blue")
        else:
            display.configure(text_color="green")

    # Close window
    def close_window():
        win.destroy()

    # Clone window next to current window
    def clone_window():
        new_x = win.winfo_x() + win.winfo_width() + 10
        new_y = win.winfo_y()
        create_rng_window(offset_x=new_x, offset_y=new_y)

    def keep_on_top():
        win.lift()
        win.attributes('-topmost', True)
        win.after(2000, keep_on_top)  # reapply every 2s

    keep_on_top()

    # Transparent root
    transparent_root = ctk.CTkFrame(win, fg_color="white", corner_radius=0)
    transparent_root.pack(fill="both", expand=True)


    # Floating frame
    floating_frame = ctk.CTkFrame(
        master=transparent_root,
        fg_color="#fefefe",
        corner_radius=0,
        width=win_width,
        height=win_height
    )
    floating_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Layout: 3 sections
    floating_frame.grid_rowconfigure(0, weight=1)
    floating_frame.grid_columnconfigure(0, weight=1)
    floating_frame.grid_columnconfigure(1, weight=2)
    floating_frame.grid_columnconfigure(2, weight=1)




    # Load your PNG
    img_path = resource_path("logo.png")
    img = Image.open(img_path).convert("RGB")  # ensure no alpha

    # Background (solid white)
    background = Image.new("RGB", img.size, (254, 254, 254))  # solid white

    # Paste logo on background WITHOUT mask
    background.paste(img, (0, 0))

    # Create CTkImage (same for light and dark to avoid recoloring)
    spawn_image = ctk.CTkImage(light_image=background, dark_image=background, size=(40, 40))

    # Spawn button with image
    spawn_btn = ctk.CTkButton(
        master=floating_frame,
        text="",  # no text
        width=40,
        height=40,
        image=spawn_image,
        fg_color="#fefefe",
        hover=False,
        corner_radius=0,
    )
    spawn_btn.grid(row=0, column=0, sticky="w", padx=0)
    # Bind double-click to spawn
    spawn_btn.bind("<Double-Button-1>", lambda e: clone_window())

    # Number display (middle)
    display = ctk.CTkButton(
        master=floating_frame,
        text="0",
        width=40,
        height=40,
        font=("Helvetica", 29, "bold"),
        fg_color="#fefefe",
        text_color="black",
        hover=False,
        corner_radius=0,
        command=generate,
        anchor="center"
    )
    display.grid(row=0, column=1, sticky="nsew", padx=0)

    # Close button (right)
    close_btn = ctk.CTkButton(
        master=floating_frame,
        text="✕",
        width=8,
        height=8,
        font=("Helvetica", 10),
        fg_color="#fefefe",
        text_color="gray",
        hover_color="#ddd",
        corner_radius=0,
        command=close_window
    )
    close_btn.grid(row=0, column=2, sticky="ne", padx=0)

    # Bind number button to click (so it doesn’t interfere with drag)
    display.bind("<Button-1>", lambda e: generate())

    # Escape closes window
    win.bind("<Escape>", lambda e: win.destroy())

    return win

# Main app root
app = ctk.CTk()
app.withdraw()

# Start with one window
create_rng_window()

app.mainloop()

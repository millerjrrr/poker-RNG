import tkinter as tk
import random
import sys
import os
from PIL import Image, ImageDraw, ImageTk

BG = "#640092"
BG_2 = "#34004d"
TEXT = "#ffffff"
PADDING = 3
RADIUS = 6
ICON_SIZE = 34

TRANSPARENT_KEY = "#ff00ff"


def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.abspath(relative_path)


class RNGWindow:
    def __init__(self, root, x=None, y=None):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg=TRANSPARENT_KEY)
        self.root.wm_attributes("-transparentcolor", TRANSPARENT_KEY)

        self.width = 100
        self.height = ICON_SIZE + PADDING * 2

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = x if x is not None else (sw - self.width) // 2
        y = y if y is not None else (sh - self.height) // 2

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.canvas = tk.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg=TRANSPARENT_KEY,
            highlightthickness=0
        )
        self.canvas.pack()

        self.draw_container()
        self.load_icon()
        self.draw_ui()
        self.make_draggable()
        self.enforce_topmost()

    # ---------- visuals ----------

    def draw_container(self):
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        d.rounded_rectangle(
            (0, 0, self.width, self.height),
            radius=RADIUS,
            fill=BG,
            outline=BG_2,
            width=2
        )

        self.bg_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.width // 2, self.height // 2, image=self.bg_img)

    def load_icon(self):
        path = resource_path("logo.png")
        icon = Image.open(path).convert("RGBA").resize((ICON_SIZE, ICON_SIZE))
        self.icon_img = ImageTk.PhotoImage(icon)

    def draw_ui(self):
        y = self.height // 2

        # icon (double-click clones)
        self.icon = self.canvas.create_image(
            ICON_SIZE // 2 + 5, y, image=self.icon_img
        )
        self.canvas.tag_bind(self.icon, "<Double-Button-1>", self.clone)

        # number
        self.number = self.canvas.create_text(
            self.width *0.6,
            y,
            text="0",
            fill=TEXT,
            font=("Helvetica", 22, "bold")
        )
        self.canvas.tag_bind(self.number, "<Button-1>", self.generate)

        # close
        self.close_btn = self.canvas.create_text(
            self.width - 12,
            10,
            text="✕",
            fill=TEXT,
            font=("Helvetica", 10, "bold")
        )
        self.canvas.tag_bind(self.close_btn, "<Button-1>", self.close)

    # ---------- behavior ----------

    def generate(self, event=None):
        self.canvas.itemconfig(self.number, text=str(random.randint(0, 99)))

    def clone(self, event=None):
        x = self.root.winfo_x() + self.width + 10
        y = self.root.winfo_y()

        new_root = tk.Toplevel()
        RNGWindow(new_root, x=x, y=y)

    def close(self, event=None):
        self.root.destroy()

    def make_draggable(self):
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

    def start_move(self, e):
        self._x = e.x
        self._y = e.y

    def do_move(self, e):
        x = self.root.winfo_pointerx() - self._x
        y = self.root.winfo_pointery() - self._y
        self.root.geometry(f"+{x}+{y}")

    def enforce_topmost(self):
        try:
            self.root.wm_attributes("-topmost", False)
            self.root.wm_attributes("-topmost", True)
            self.root.lift()
        except:
            pass

        # run again every 800ms
        self.root.after(800, self.enforce_topmost)


# ---------- run ----------
if __name__ == "__main__":
    root = tk.Tk()
    RNGWindow(root)
    root.mainloop()

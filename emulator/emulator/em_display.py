import tkinter as tk
from PIL import Image, ImageTk, Image
import queue

SCREEN_WIDTH = 296  
SCREEN_HEIGHT = 128  


class Emulator:
    def __init__(self):
        self.screen = None
        self.root = None
        self.tk_img = None
        self.button_events = queue.Queue()
        self.display_canvas = None

        self._init_gui()

    def _init_gui(self):
        self.root = tk.Tk()
        self.root.title("EPD Simulator")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Landscape-oriented frame (swap W & H)
        canvas_frame = tk.Frame(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        canvas_frame.pack_propagate(0)
        canvas_frame.pack(pady=5)

        self.display_canvas = tk.Label(canvas_frame, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.display_canvas.pack()

        # Buttons below
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        for i in range(3):
            tk.Button(
                btn_frame,
                text=f"Button {i + 1}",
                command=lambda i=i: self._push_button(i)
            ).pack(side=tk.LEFT, padx=5)

    def _push_button(self, button_id):
        self.button_events.put(button_id)

    def _on_close(self):
        self.root.quit()
        self.root.destroy()

    def mainloop(self):
        self.root.mainloop()

    def set_refresh_mode_full(self):
        # Hardware method
        pass

    def set_refresh_mode_partial(self):
        # Hardware method
        pass

    def clear(self):
        blank = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.display(blank)


    def display(self, image):
        self.tk_img = ImageTk.PhotoImage(image)
        self.display_canvas.config(image=self.tk_img)

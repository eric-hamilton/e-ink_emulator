from emulator.fonts import create_font
from PIL import Image, ImageDraw
from datetime import datetime
from emulator.config import SCREEN_HEIGHT, SCREEN_WIDTH
import os

def get_dummy_data():
    # Replace this logic with whatever data you want and how to get it
    return {
        "time_str": "06:20",
        "ampm": "am",
        "temp": 69,
        "date_str": "2025-05-24",
        "weather_icon": None,
        "error_code": None,
    }

class Screen:
    def __init__(self, update_interval):
        self.update_interval = update_interval  # in seconds

    def update(self):
        """Override this in subclasses to draw the screen."""
        raise NotImplementedError

        
class ClockScreen(Screen):
    def __init__(self, app):
        super().__init__(update_interval=6)  # every 6 seconds
        self.app = app

        # Fonts
        self.time_font = create_font('some_font.ttf', 86)
        self.ampm_font = create_font('some_font.ttf', 18)
        self.temp_font = create_font('some_font.ttf', 32)
        self.date_font = create_font('some_font.ttf', 32)

        # Layout
        self.weather_icon_size = 64
        self.error_icon_size = 32
        self.weather_icon_area = (0, 0)
        self.error_icon_area = (SCREEN_WIDTH - self.error_icon_size, 0)

        self.time_y = 0
        self.temp_y = 69
        self.date_y = 92

        # Previous state
        self.previous_data = {
            "time_str": "HELLO THERE",
            "ampm": "am",
            "temp": 69,
            "date_str": "2025-05-24",
            "weather_icon": None,
            "error_code": None,
        }
        self.app.panel.set_refresh_mode_partial()

    def update(self):
        do_update = False
        canvas = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        draw = ImageDraw.Draw(canvas)

        # Get data
        current_data = get_dummy_data()


        # Weather icon
        if current_data["weather_icon"] != self.previous_data["weather_icon"]:
            weather_icon_path = current_data["weather_icon"]
            icon = Image.open(weather_icon_path).resize((self.weather_icon_size, self.weather_icon_size))
            canvas.paste(icon, self.weather_icon_area)
            self.previous_data["weather_icon"] = weather_icon_path
            do_update = True

        # Temperature
        if current_data["temp"] != self.previous_data["temp"] or do_update:
            temp = str(current_data["temp"])
            temp_size = draw.textsize(temp, font=self.temp_font)
            temp_x = int((self.weather_icon_size / 2) - (temp_size[0] / 2))
            draw.text((temp_x, self.temp_y), temp, font=self.temp_font, fill=0)
            do_update = True

        # Time
        if current_data["time_str"] != self.previous_data["time_str"] or do_update:
            time_str = current_data["time_str"]
            time_size = draw.textsize(time_str, font=self.time_font)
            time_x = int((SCREEN_WIDTH / 2) - (time_size[0] / 2) + self.error_icon_size / 2)
            draw.text((time_x, self.time_y), time_str, font=self.time_font, fill=0)
            do_update = True

        # AM/PM
        if current_data["ampm"] != self.previous_data["ampm"] or do_update:
            ampm = current_data["ampm"]
            ampm_size = draw.textsize(ampm, font=self.ampm_font)
            ampm_x = time_x + time_size[0] + 2
            ampm_y = self.time_y + time_size[1] - ampm_size[1]
            draw.text((ampm_x, ampm_y), ampm, font=self.ampm_font, fill=0)
            do_update = True

        # Date
        if current_data["date_str"] != self.previous_data["date_str"] or do_update:
            date_str = current_data["date_str"]
            date_size = draw.textsize(date_str, font=self.date_font)
            date_x = SCREEN_WIDTH - date_size[0] - 5
            draw.text((date_x, self.date_y), date_str, font=self.date_font, fill=0)
            do_update = True

        # Error icon
        if current_data["error_code"] != self.previous_data["error_code"] or do_update:
            error_code = current_data["error_code"]
            if error_code != None:
                icon_name = {
                    0: "x.png",
                    1: "noNetwork.png",
                    2: "pcDisconnected.png"
                }.get(error_code, "x.png")

                icon_path = os.path.join("some icon directory", icon_name)
                icon = Image.open(icon_path).resize((self.error_icon_size, self.error_icon_size))
                canvas.paste(icon, self.error_icon_area)
                self.previous_data["error"] = error_code
                do_update = True

        if do_update:
            self.app.panel.display(canvas)
        self.previous_data = current_data
        
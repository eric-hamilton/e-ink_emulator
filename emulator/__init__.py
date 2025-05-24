

import queue
from time import sleep, time

from emulator.config import BUTTON_1, BUTTON_2, BUTTON_3
from emulator.screens import ClockScreen


class Emulator():
    def __init__(self):
        
        self.button_events = queue.Queue()
        try:
            import RPi.GPIO as GPIO
            # pi
            GPIO.setmode(GPIO.BCM)
            from emulator.hardware.epd_panel import EPD
            from emulator.hardware.input import InputHandler
            self.panel = EPD()
            self.panel.set_refresh_mode_full()
            self.button_watcher = InputHandler(self.button_events)
        except ImportError as e:
            # windows
            from emulator.emulator.em_display import Emulator
            self.panel = Emulator()
            from emulator.emulator.em_input import InputHandler
            self.button_watcher = InputHandler(self.button_events, self.panel)
        

        
        
    
    def run(self):
        self.current_screen = ClockScreen(self)
        self.running = True
        self.button_watcher.start()
        self.panel.clear()
        last_screen_update = 0  # timestamp of last update

        try:
            while self.running:
                # Handle any button events
                self.process_buttons()

                now = time()
                if now - last_screen_update >= self.current_screen.update_interval:
                    self.current_screen.update()
                    last_screen_update = now

                sleep(0.05)

        except KeyboardInterrupt:
            print("Exiting.")
        finally:
            self.button_watcher.stop()
    
    
    def process_buttons(self):
        while not self.button_events.empty():
            pin = self.button_events.get()
            if pin == BUTTON_1:
                print("Button 1 pressed: Main screen")
            elif pin == BUTTON_2:
                print("Button 2 pressed: Menu screen")

            elif pin == BUTTON_3:
                print("Button 3 pressed: Force refresh")
                
    

def create_app():
    app = Emulator()
    return app
    

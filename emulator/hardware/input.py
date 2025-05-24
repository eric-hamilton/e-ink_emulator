import RPi.GPIO as GPIO
import threading
from time import sleep
from emulator.config import BUTTON_PINS

class InputHandler(threading.Thread):
    def __init__(self, event_queue, bounce_time=200):
        """
        bounce_time: debounce time in milliseconds
        """
        super().__init__(daemon=True)
        self.queue = event_queue
        self.bounce_time = bounce_time
        self._running = True
        for pin in BUTTON_PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING,
                callback=self._callback,
                bouncetime=self.bounce_time
            )

    def _callback(self, pin):
        """Callback function to handle button press"""
        self.queue.put(pin)

    def run(self):
        
        while self._running:
            sleep(0.1)

    def stop(self):
        self._running = False
        for pin in BUTTON_PINS:
            GPIO.remove_event_detect(pin)
        GPIO.cleanup()

import threading
from time import sleep
from emulator.config import BUTTON_1, BUTTON_2, BUTTON_3

class InputHandler(threading.Thread):
    def __init__(self, event_queue, simulator, poll_interval=0.05):
        super().__init__(daemon=True)
        self.queue = event_queue
        self.simulator = simulator
        self.poll_interval = poll_interval
        self._running = True

    def run(self):
        while self._running:
            while not self.simulator.button_events.empty():
                button_id = self.simulator.button_events.get()
                if button_id == 0:
                    self.queue.put(BUTTON_1)
                elif button_id == 1:
                    self.queue.put(BUTTON_2)
                elif button_id == 2:
                    self.queue.put(BUTTON_3)
            sleep(self.poll_interval)

    def stop(self):
        self._running = False

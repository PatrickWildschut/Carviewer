import threading
import time

LONG_PRESS_SECONDS = 1.0


class InfoButton:
    """Splits the info button into short presses (fired on release) and long presses.

    A long press ticks once per LONG_PRESS_SECONDS while the button is held, the first
    tick at the moment the hold counts as long.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._down = False
        self._down_since = 0.0
        self._ticks_seen = 0
        self._short_pending = False
        self._cruise_short_pending = False
        self._long_pending = 0

    def _update(self, pressed):
        now = time.monotonic()
        if pressed and not self._down:
            self._down = True
            self._down_since = now
            self._ticks_seen = 0
        elif pressed:
            ticks = int((now - self._down_since) / LONG_PRESS_SECONDS)
            if ticks > self._ticks_seen:
                self._long_pending += ticks - self._ticks_seen
                self._ticks_seen = ticks
        elif self._down:
            self._down = False
            if self._ticks_seen == 0:
                self._short_pending = True
                self._cruise_short_pending = True

    def short_pressed(self, pressed):
        with self._lock:
            self._update(pressed)
            result, self._short_pending = self._short_pending, False
            return result

    def cruise_short_pressed(self, pressed):
        # separate flag so the cruise thread and the screens each see every short press
        with self._lock:
            self._update(pressed)
            result, self._cruise_short_pending = self._cruise_short_pending, False
            return result

    def long_ticks(self, pressed):
        # number of long press ticks since the last call
        with self._lock:
            self._update(pressed)
            result, self._long_pending = self._long_pending, 0
            return result

    def held(self, pressed):
        # True while the button is down
        with self._lock:
            self._update(pressed)
            return self._down

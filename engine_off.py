import os
import threading
import time
import pygame

# Shuts the Pi down once the engine has been switched off.
# Arms after the engine has actually run. As soon as RPM reads 0 a "Bye!" text
# fades in over FADE_TIME seconds and then the shutdown command runs. If RPM
# goes above 0 again during the fade, or the screen is touched, the shutdown is
# cancelled. After a touch it stays disarmed until the engine runs again.
FADE_TIME = 1

_start = None
_touched = threading.Event()

def _draw_bye():
    start = _start
    if start is None:
        return
    surface = pygame.display.get_surface()
    if surface is None:
        return
    progress = min(1.0, (time.time() - start) / FADE_TIME)

    width, height = surface.get_size()
    dim = pygame.Surface((width, height))
    dim.set_alpha(int(220 * progress))
    surface.blit(dim, (0, 0))

    text = pygame.font.Font(None, height // 4).render("Bye!", True, (255, 255, 255))
    text.set_alpha(int(255 * progress))
    surface.blit(text, text.get_rect(center=(width // 2, height // 2)))

# Every screen ends its frame with pygame.display.flip(), so hooking it draws
# the overlay on top of whichever screen is showing (on the main thread).
_original_flip = pygame.display.flip
def _flip():
    _draw_bye()
    _original_flip()
pygame.display.flip = _flip

# Screens read their input with pygame.event.get(), so hook it to see touches
# during the fade. The touch is swallowed so it doesn't press a button underneath.
_TOUCH_EVENTS = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.FINGERDOWN, pygame.FINGERUP)
_original_get = pygame.event.get
def _get(*args, **kwargs):
    events = _original_get(*args, **kwargs)
    if _start is None:
        return events
    if any(event.type in _TOUCH_EVENTS for event in events):
        _touched.set()
    return [event for event in events if event.type not in _TOUCH_EVENTS]
pygame.event.get = _get

def _watch(get_rpm, shutdown):
    global _start
    armed = False
    while True:
        if get_rpm() > 0:
            armed = True
        elif armed:
            _touched.clear()
            _start = time.time()
            while time.time() - _start < FADE_TIME:
                time.sleep(0.05)
                if get_rpm() > 0:
                    _start = None
                    break
                if _touched.is_set():
                    _start = None
                    armed = False
                    break
            else:
                shutdown()
                return
        time.sleep(0.1)

def start(get_rpm, shutdown=lambda: os.system("shutdown now")):
    threading.Thread(target=_watch, args=(get_rpm, shutdown), daemon=True).start()

import i3ipc
import time

i3 = i3ipc.Connection()

def find_window_by_class(i3, class_name):
    return next(
        (w for w in i3.get_tree().leaves() if w.window_class == class_name),
        None
    )

sublime = find_window_by_class(i3, "Sublime_text")

time.sleep(5)
sublime.command("move to scratchpad")
time.sleep(5)
sublime.command("scratchpad show")
sublime.command("fullscreen enable")

from screeninfo import get_monitors

def center_window(window):
    """
    Center a window on the screen.

    Parameters:
    window (Tkinter.Tk or Tkinter.Toplevel): The window to be centered.

    Updates the size and position of the window to center it on the screen.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    monitors = get_monitors()
    primary_monitor = next((monitor for monitor in monitors if monitor.is_primary), monitors[0])

    x = (primary_monitor.width - width) // 2 + primary_monitor.x
    y = (primary_monitor.height - height) // 2 + primary_monitor.y

    window.geometry(f'{width}x{height}+{x}+{y}')

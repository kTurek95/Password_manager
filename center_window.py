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
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

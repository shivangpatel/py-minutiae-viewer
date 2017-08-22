from pathlib import Path
from tkinter import Tk, PhotoImage

from pyminutiaeviewer import gui

root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.title("Py Minutiae Viewer")
img = PhotoImage(file=Path(__file__).resolve().parent / 'pyminutiaeviewer' / 'images' / 'icon.png')
root.iconphoto(True, img)
app = gui.Root(root)
app.mainloop()
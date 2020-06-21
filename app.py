import tkinter as tk
from tkinter import filedialog, Listbox
from PyPDF2 import PdfFileMerger, utils
import os

files = []
destination = "D:/Bruce/Documents/"

root = tk.Tk()


def center_window():
    root.withdraw()
    root.update_idletasks()  # Update "requested size" from geometry manager

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    root.deiconify()


def addFile():
    filename = filedialog.askopenfilenames(initialdir="/", title="Select Files",
                                           filetypes=(("PDF", "*.pdf"), ("All Files", "*.*")))
    for file in filename:
        files.append(file)
        label = tk.Label(frame, text=file[file.rfind(
            "/")+1:], bg="grey", justify="left", font=("Helvetica", 12))
        label.pack()


def convertFiles():
    merger = PdfFileMerger()

    if len(files) > 0:
        for file in files:
            merger.append(file)
        if not os.path.exists(destination + 'merged.pdf'):
            merger.write(destination + 'Merged.pdf')
    merger.close()


def clearFiles():
    for widget in frame.winfo_children():
        widget.destroy()
    files.clear()


canvas = tk.Canvas(root, height=600, width=600, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(width=500, height=400, relx=0.1, rely=0.1)

scrollbars = tk.Scrollbar(frame, bg="black", orient="vertical")
scrollbars.pack(side="right", fill="y")

openFile = tk.Button(root, text="Open File", padx=10, pady=5,
                     bg="#263D42", fg="white", command=addFile)
openFile.place(x=100, y=500)

convertFiles = tk.Button(root, text="Convert Files", fg="white",
                         bg="#263D42", padx=10, pady=5, command=convertFiles)
convertFiles.place(x=200, y=500)

clear = tk.Button(root, text="Clear", padx=10, pady=5,
                  bg="#263D42", fg="white", command=clearFiles)
clear.place(x=320, y=500)

center_window()

root.mainloop()

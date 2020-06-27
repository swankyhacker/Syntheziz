from tkinter import *
from tkinter import filedialog, Listbox
from PyPDF2 import PdfFileMerger, utils
import os

files = []
destination = "D:/Bruce/Documents/"

root = Tk()
root.geometry("630x650")
root.configure(bg="#263D42")


def addFile():
    selectedFiles = filedialog.askopenfilenames(initialdir="/", title="Select Files",
                                                filetypes=(("PDF", "*.pdf"), ("All Files", "*.*")))
    for file in selectedFiles:
        files.append(file)
        fileName = file[file.rfind("/")+1:]
        label = Label(frame, text=f"~{fileName}", bg="#263D42", fg="white", width=20, anchor=W,
                      font=("Helvetica", 12))
        label.grid()


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


frame = Frame(root, bg="white", width=560, height=400)
frame.grid_propagate(0)
frame.grid(row=0, column=0, padx=30, pady=30, columnspan=6, rowspan=6)

destAddress_label = Label(
    root, text="Destination Address:", bg="#263D42", fg="white")
destAddress_label.grid(row=7, column=0)

destAddress = Entry(root, width=50)
destAddress.grid(row=7, column=1, columnspan=3)

findPath = Button(root, bg="#263D42", fg="white", text="...")
findPath.grid(row=7, column=4)

deleteFiles = Checkbutton(
    root, text="Delete files after merging", bg="#263D42", fg="white")
deleteFiles.grid(row=9, column=0)

openFile = Button(root, text="Open File", padx=10, pady=5, width=10,
                  bg="#263D42", fg="white", command=addFile)
openFile.grid(row=7, column=5)

convertFiles = Button(root, text="Convert Files", fg="white", width=10,
                      bg="#263D42", padx=10, pady=5, command=convertFiles)
convertFiles.grid(row=8, column=5, pady=15)

clear = Button(root, text="Clear", padx=10, pady=5, width=10,
               bg="#263D42", fg="white", command=clearFiles)
clear.grid(row=9, column=5)

root.mainloop()

# # Grid
# Order of files
# delete files
# change destination
# Exceptions
# design
# file duplication
